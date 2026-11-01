from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


class Profile(models.Model):
    """Datos personales del portfolio. Es un único registro (singleton)."""

    full_name = models.CharField("nombre completo", max_length=120)
    headline = models.CharField(
        "titular", max_length=150, help_text="Ej: Backend Developer · Python & Django"
    )
    tagline = models.CharField(
        "frase de presentación",
        max_length=240,
        blank=True,
        help_text="Texto corto que aparece debajo del nombre en el inicio.",
    )
    short_bio = models.TextField(
        "biografía corta",
        blank=True,
        help_text="Se usa en el inicio y como resumen del CV.",
    )
    bio = models.TextField(
        "biografía completa",
        blank=True,
        help_text="Se muestra en 'Sobre mí'. Podés separar párrafos con líneas en blanco.",
    )
    email = models.EmailField("email de contacto")
    phone = models.CharField("teléfono", max_length=40, blank=True)
    location = models.CharField(
        "ubicación", max_length=120, blank=True, default="Buenos Aires, Argentina"
    )
    availability = models.CharField(
        "disponibilidad",
        max_length=120,
        blank=True,
        default="Abierto a nuevas oportunidades",
    )
    avatar = models.ImageField(
        "foto de perfil", upload_to="profile/", blank=True, null=True
    )
    github_url = models.URLField("GitHub", blank=True)
    linkedin_url = models.URLField("LinkedIn", blank=True)
    twitter_url = models.URLField("X / Twitter", blank=True)
    website_url = models.URLField("Sitio web", blank=True)
    years_experience = models.PositiveSmallIntegerField(
        "años de experiencia", default=2
    )
    cv_summary = models.TextField(
        "resumen para el CV",
        blank=True,
        help_text="Si lo dejás vacío se usa la biografía corta.",
    )
    updated_at = models.DateTimeField("actualizado el", auto_now=True)

    class Meta:
        verbose_name = "perfil"
        verbose_name_plural = "perfil"

    def __str__(self) -> str:
        return self.full_name

    def save(self, *args, **kwargs):
        # Garantiza que exista un solo perfil (pk=1).
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Evita quedarse sin perfil por accidente.
        return None

    @property
    def initials(self) -> str:
        parts = [part for part in self.full_name.split() if part]
        if not parts:
            return "?"
        if len(parts) == 1:
            return parts[0][0].upper()
        return (parts[0][0] + parts[-1][0]).upper()

    @property
    def cv_pdf_filename(self) -> str:
        return f"CV-{slugify(self.full_name)}.pdf"


class Education(models.Model):
    """Formación académica."""

    institution = models.CharField("institución", max_length=160)
    degree = models.CharField("carrera / título", max_length=180)
    start_date = models.DateField(
        "fecha de inicio",
        blank=True,
        null=True,
        help_text="Opcional si solo se conoce que la formación está en curso.",
    )
    end_date = models.DateField("fecha de fin", blank=True, null=True)
    is_current = models.BooleanField("en curso", default=False)
    description = models.TextField("descripción", blank=True)
    order = models.PositiveSmallIntegerField("orden", default=0)

    class Meta:
        verbose_name = "formación"
        verbose_name_plural = "formación"
        ordering = ["order", "-start_date"]

    def __str__(self) -> str:
        return f"{self.degree} · {self.institution}"

    @property
    def date_range(self) -> str:
        if self.start_date:
            start = self.start_date.strftime("%m/%Y")
            if self.is_current:
                return f"{start} – Actualidad"
            if self.end_date:
                return f"{start} – {self.end_date.strftime('%m/%Y')}"
            return start
        if self.is_current:
            return "En curso"
        if self.end_date:
            return f"Hasta {self.end_date.strftime('%m/%Y')}"
        return ""


class Certification(models.Model):
    """Cursos y certificaciones complementarias."""

    name = models.CharField("curso / certificación", max_length=180)
    issuer = models.CharField("institución", max_length=140)
    year = models.PositiveSmallIntegerField("año", blank=True, null=True)
    description = models.TextField("descripción", blank=True)
    url = models.URLField("enlace", blank=True)
    order = models.PositiveSmallIntegerField("orden", default=0)

    class Meta:
        verbose_name = "curso / certificación"
        verbose_name_plural = "cursos y certificaciones"
        ordering = ["order", "-year", "name"]

    def __str__(self) -> str:
        return f"{self.name} · {self.issuer}"

    @property
    def date_label(self) -> str:
        return str(self.year) if self.year else ""


class Skill(models.Model):
    """Habilidades técnicas agrupadas por categoría."""

    class Category(models.TextChoices):
        LANGUAGES = "languages", "Lenguajes"
        BACKEND = "backend", "Backend"
        DATABASE = "database", "Bases de datos"
        TOOLS = "tools", "Herramientas"
        FRONTEND = "frontend", "Frontend"

    name = models.CharField("nombre", max_length=80)
    category = models.CharField(
        "categoría", max_length=20, choices=Category.choices, default=Category.BACKEND
    )
    level = models.PositiveSmallIntegerField(
        "nivel", default=80, help_text="Porcentaje de 0 a 100."
    )
    icon = models.CharField(
        "icono",
        max_length=8,
        blank=True,
        help_text="Opcional: un emoji o símbolo corto (ej: 🐍).",
    )
    is_featured = models.BooleanField("destacada", default=False)
    order = models.PositiveSmallIntegerField("orden", default=0)

    class Meta:
        verbose_name = "skill"
        verbose_name_plural = "skills"
        ordering = ["category", "order", "name"]

    def __str__(self) -> str:
        return f"{self.name} ({self.get_category_display()})"

    def save(self, *args, **kwargs):
        self.level = max(0, min(100, self.level))
        super().save(*args, **kwargs)


def current_year() -> int:
    return timezone.localdate().year


class Project(models.Model):
    """Proyecto publicado en el portfolio."""

    title = models.CharField("título", max_length=150)
    slug = models.SlugField("slug", max_length=170, unique=True, blank=True)
    year = models.PositiveSmallIntegerField("año", default=current_year)
    short_description = models.CharField(
        "descripción corta",
        max_length=260,
        help_text="Aparece en las tarjetas del listado de proyectos.",
    )
    description = models.TextField(
        "descripción completa",
        help_text="Podés separar párrafos con líneas en blanco.",
    )
    technologies = models.CharField(
        "tecnologías",
        max_length=240,
        help_text="Separadas por comas. Ej: Python, Django, MySQL, Docker",
    )
    repository_url = models.URLField("repositorio de GitHub", blank=True)
    demo_url = models.URLField("demostración", blank=True)
    image = models.ImageField(
        "imagen", upload_to="projects/", blank=True, null=True
    )
    is_featured = models.BooleanField("destacado", default=False)
    is_published = models.BooleanField("publicado", default=True)
    order = models.PositiveSmallIntegerField("orden", default=0)
    created_at = models.DateTimeField("creado el", auto_now_add=True)
    updated_at = models.DateTimeField("actualizado el", auto_now=True)

    class Meta:
        verbose_name = "proyecto"
        verbose_name_plural = "proyectos"
        ordering = ["order", "-created_at"]

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)[:150] or "proyecto"
            slug = base
            counter = 2
            while Project.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse("project_detail", kwargs={"slug": self.slug})

    @property
    def technology_list(self) -> list[str]:
        return [tech.strip() for tech in self.technologies.split(",") if tech.strip()]

    @property
    def initials(self) -> str:
        stopwords = {
            "a", "al", "con", "de", "del", "e", "el", "en", "la", "las",
            "los", "o", "para", "por", "y",
        }
        words = [word for word in self.title.split() if word]
        significant = [word for word in words if word.lower() not in stopwords]
        words = significant or words
        if not words:
            return "P"
        if len(words) == 1:
            return words[0][:2].upper()
        return (words[0][0] + words[1][0]).upper()


class Experience(models.Model):
    """Experiencia laboral, freelance y proyectos personales."""

    class Kind(models.TextChoices):
        WORK = "work", "Experiencia laboral"
        FREELANCE = "freelance", "Freelance"
        PERSONAL = "personal", "Proyecto personal"

    role = models.CharField("puesto / rol", max_length=150)
    company = models.CharField("empresa / proyecto", max_length=150)
    kind = models.CharField(
        "tipo", max_length=20, choices=Kind.choices, default=Kind.WORK
    )
    location = models.CharField("ubicación", max_length=120, blank=True)
    start_date = models.DateField("fecha de inicio")
    end_date = models.DateField("fecha de fin", blank=True, null=True)
    is_current = models.BooleanField("actual", default=False)
    description = models.TextField(
        "descripción",
        help_text="Una línea por viñeta. Se muestran como lista.",
    )
    technologies = models.CharField(
        "tecnologías", max_length=240, blank=True, help_text="Separadas por comas."
    )
    url = models.URLField("enlace", blank=True)
    order = models.PositiveSmallIntegerField("orden", default=0)

    class Meta:
        verbose_name = "experiencia"
        verbose_name_plural = "experiencia"
        ordering = ["order", "-start_date"]

    def __str__(self) -> str:
        return f"{self.role} · {self.company}"

    @property
    def date_range(self) -> str:
        start = self.start_date.strftime("%m/%Y")
        if self.is_current:
            return f"{start} – Actualidad"
        if self.end_date:
            return f"{start} – {self.end_date.strftime('%m/%Y')}"
        return start

    @property
    def technology_list(self) -> list[str]:
        return [tech.strip() for tech in self.technologies.split(",") if tech.strip()]

    @property
    def is_personal(self) -> bool:
        return self.kind == self.Kind.PERSONAL


class ContactMessage(models.Model):
    """Mensajes recibidos desde el formulario de contacto."""

    name = models.CharField("nombre", max_length=120)
    email = models.EmailField("email")
    company = models.CharField("empresa", max_length=140, blank=True)
    subject = models.CharField("asunto", max_length=180, blank=True)
    message = models.TextField("mensaje")
    created_at = models.DateTimeField("recibido el", default=timezone.now)
    is_read = models.BooleanField("leído", default=False)
    ip_address = models.GenericIPAddressField("IP", blank=True, null=True)

    class Meta:
        verbose_name = "mensaje de contacto"
        verbose_name_plural = "mensajes de contacto"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.name} <{self.email}>"
