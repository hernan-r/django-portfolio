from django.contrib import admin, messages
from django.utils.html import format_html

from .models import (
    Certification,
    ContactMessage,
    Education,
    Experience,
    Profile,
    Project,
    Skill,
)

admin.site.site_header = "Portfolio · Administración"
admin.site.site_title = "Portfolio"
admin.site.index_title = "Gestión de contenido"
admin.site.site_url = "/"


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Identidad",
            {
                "fields": (
                    "full_name",
                    "headline",
                    "tagline",
                    "avatar",
                    "avatar_preview",
                )
            },
        ),
        (
            "Biografía",
            {
                "fields": ("short_bio", "bio", "cv_summary"),
                "description": "Estos textos alimentan el inicio, 'Sobre mí' y el CV en PDF.",
            },
        ),
        (
            "Contacto",
            {"fields": ("email", "phone", "location", "availability")},
        ),
        (
            "Redes y enlaces",
            {"fields": ("github_url", "linkedin_url", "twitter_url", "website_url")},
        ),
        (
            "Datos para el CV",
            {
                "fields": (
                    "years_experience",
                    "cv_headline",
                    "cv_phone",
                    "soft_skills",
                    "updated_at",
                ),
                "description": (
                    "Estos campos solo se usan en el PDF descargable. "
                    "El teléfono del CV no se publica en el sitio."
                ),
            },
        ),
    )
    readonly_fields = ("avatar_preview", "updated_at")

    @admin.display(description="Vista previa")
    def avatar_preview(self, obj):
        if obj and obj.avatar:
            return format_html(
                '<img src="{}" alt="Foto de perfil" style="max-height:120px;border-radius:10px;" />',
                obj.avatar.url,
            )
        return "Sin foto cargada (se muestra un monograma)."

    def has_add_permission(self, request):
        return not Profile.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        # Si no existe el perfil, redirige directo al formulario de creación.
        if not Profile.objects.exists():
            return self.add_view(request)
        return super().changelist_view(request, extra_context)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "level",
        "is_featured",
        "show_in_cv",
        "order",
    )
    list_editable = ("level", "is_featured", "show_in_cv", "order")
    list_filter = ("category", "is_featured", "show_in_cv")
    search_fields = ("name",)
    ordering = ("category", "order", "name")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "year",
        "is_featured",
        "is_published",
        "order",
        "updated_at",
    )
    list_editable = ("is_featured", "is_published", "order")
    list_filter = ("is_published", "is_featured", "created_at")
    search_fields = ("title", "short_description", "description", "technologies")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("image_preview", "created_at", "updated_at")
    fieldsets = (
        (
            "Información principal",
            {"fields": ("title", "slug", "short_description", "description")},
        ),
        (
            "Tecnologías y enlaces",
            {
                "fields": (
                    "technologies",
                    "repository_url",
                    "demo_url",
                ),
                "description": "Tecnologías separadas por comas. Ej: Python, Django, MySQL.",
            },
        ),
        (
            "Imagen",
            {
                "fields": ("image", "image_preview"),
                "description": "Opcional. Si no cargás una, se usa una portada generada.",
            },
        ),
        (
            "Publicación",
            {
                "fields": ("year", "is_featured", "is_published", "order", "created_at", "updated_at"),
                "description": "Los proyectos destacados aparecen en el inicio.",
            },
        ),
    )

    @admin.display(description="Vista previa")
    def image_preview(self, obj):
        if obj and obj.image:
            return format_html(
                '<img src="{}" alt="{}" style="max-height:160px;border-radius:10px;" />',
                obj.image.url,
                obj.title,
            )
        return "Sin imagen."


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("role", "company", "kind", "date_range", "is_current", "order")
    list_filter = ("kind", "is_current")
    search_fields = ("role", "company", "description", "technologies")
    list_editable = ("order",)
    fieldsets = (
        (
            "Puesto",
            {"fields": ("role", "company", "kind", "location")},
        ),
        (
            "Fechas",
            {"fields": ("start_date", "end_date", "is_current", "date_label")},
        ),
        (
            "Detalle",
            {
                "fields": ("description", "technologies", "url", "order"),
                "description": "En la descripción, escribí una viñeta por línea.",
            },
        ),
    )


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ("degree", "institution", "date_range", "is_current", "order")
    list_filter = ("is_current", "institution")
    search_fields = ("degree", "institution", "description")
    list_editable = ("order",)
    fieldsets = (
        ("Formación", {"fields": ("degree", "institution", "description")}),
        ("Fechas", {"fields": ("start_date", "end_date", "is_current", "order")}),
    )


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ("name", "issuer", "year", "order")
    list_filter = ("issuer", "year")
    search_fields = ("name", "issuer", "description")
    list_editable = ("order",)
    fieldsets = (
        ("Curso / certificación", {"fields": ("name", "issuer", "year")}),
        ("Detalle", {"fields": ("description", "url", "order")}),
    )


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "company",
        "subject",
        "created_at",
        "is_read",
    )
    list_filter = ("is_read", "created_at")
    search_fields = ("name", "email", "company", "subject", "message")
    date_hierarchy = "created_at"
    readonly_fields = (
        "name",
        "email",
        "company",
        "subject",
        "message",
        "created_at",
        "ip_address",
    )
    actions = ("mark_as_read", "mark_as_unread")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        # Permite abrir el detalle (solo lectura) desde el listado.
        return True

    @admin.action(description="Marcar como leídos")
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(
            request, f"{updated} mensaje(s) marcados como leídos.", messages.SUCCESS
        )

    @admin.action(description="Marcar como no leídos")
    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(
            request, f"{updated} mensaje(s) marcados como no leídos.", messages.SUCCESS
        )
