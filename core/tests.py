from datetime import date

from django.test import TestCase
from django.urls import reverse

from .forms import ContactForm
from .models import (
    Certification,
    ContactMessage,
    Education,
    Experience,
    Profile,
    Project,
    Skill,
)


def create_profile(**overrides):
    data = {
        "full_name": "Test Dev",
        "headline": "Backend Developer",
        "tagline": "Construyo APIs con Django.",
        "short_bio": "Backend developer de prueba.",
        "bio": "Primer párrafo.\n\nSegundo párrafo.",
        "email": "test@example.com",
        "location": "Buenos Aires, Argentina",
        "years_experience": 4,
    }
    data.update(overrides)
    profile, _ = Profile.objects.update_or_create(pk=1, defaults=data)
    return profile


class ProfileModelTests(TestCase):
    def test_profile_is_a_singleton(self):
        create_profile(full_name="Primero")
        create_profile(full_name="Segundo")

        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(Profile.objects.get(pk=1).full_name, "Segundo")

    def test_initials_for_one_and_multiple_words(self):
        self.assertEqual(create_profile(full_name="Hernán").initials, "H")
        self.assertEqual(create_profile(full_name="Hernán García").initials, "HG")

    def test_cv_filename(self):
        profile = create_profile(full_name="Hernán García")
        self.assertEqual(profile.cv_pdf_filename, "CV-hernan-garcia.pdf")


class ProjectModelTests(TestCase):
    def test_slug_is_generated_and_unique(self):
        first = Project.objects.create(
            title="API de Turnos",
            short_description="Descripción",
            description="Detalle",
            technologies="Python, Django",
        )
        second = Project.objects.create(
            title="API de Turnos",
            short_description="Descripción",
            description="Detalle",
            technologies="Java, Spring Boot",
        )

        self.assertEqual(first.slug, "api-de-turnos")
        self.assertEqual(second.slug, "api-de-turnos-2")

    def test_technologies_are_split(self):
        project = Project.objects.create(
            title="Proyecto",
            short_description="Descripción",
            description="Detalle",
            technologies="Python, Django , MySQL,",
        )
        self.assertEqual(project.technology_list, ["Python", "Django", "MySQL"])

    def test_initials_skip_stopwords(self):
        project = Project.objects.create(
            title="API de Gestión de Turnos",
            short_description="Descripción",
            description="Detalle",
            technologies="Python",
        )
        self.assertEqual(project.initials, "AG")


class PageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # La migración de datos crea contenido de ejemplo; lo limpiamos para
        # que estos tests sean deterministas.
        for model in (
            Project,
            Skill,
            Experience,
            Education,
            Certification,
            Profile,
            ContactMessage,
        ):
            model.objects.all().delete()

        cls.profile = create_profile()
        Education.objects.create(
            institution="UTN",
            degree="Ingeniería en Sistemas",
            start_date=date(2021, 3, 1),
            is_current=True,
        )
        Skill.objects.create(name="Python", category="languages", level=90, is_featured=True)
        Skill.objects.create(name="Django", category="backend", level=90, is_featured=True)
        cls.published = Project.objects.create(
            title="Proyecto Python",
            short_description="Un proyecto con Django.",
            description="Descripción completa del proyecto.",
            technologies="Python, Django",
            repository_url="https://github.com/example/proyecto",
            is_featured=True,
        )
        cls.unpublished = Project.objects.create(
            title="Proyecto Oculto",
            short_description="No debería verse.",
            description="Oculto.",
            technologies="Java",
            is_published=False,
        )
        Experience.objects.create(
            role="Backend Developer",
            company="Acme",
            kind=Experience.Kind.WORK,
            start_date=date(2024, 1, 1),
            is_current=True,
            description="Desarrollo de APIs.",
            technologies="Python, Django",
        )
        Experience.objects.create(
            role="Proyecto propio",
            company="Side project",
            kind=Experience.Kind.PERSONAL,
            start_date=date(2023, 1, 1),
            end_date=date(2023, 12, 1),
            description="Automatizaciones.",
            technologies="Python",
        )

    def test_public_pages_render(self):
        names = ["home", "about", "skills", "projects", "experience", "contact"]
        for name in names:
            with self.subTest(page=name):
                response = self.client.get(reverse(name))
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, "Test Dev")

    def test_project_detail_renders_published_project(self):
        response = self.client.get(self.published.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Proyecto Python")
        self.assertContains(response, "Python")

    def test_project_detail_hides_unpublished_project(self):
        response = self.client.get(self.unpublished.get_absolute_url())
        self.assertEqual(response.status_code, 404)

    def test_project_search_and_technology_filter(self):
        response = self.client.get(reverse("projects"), {"q": "django"})
        self.assertContains(response, "Proyecto Python")
        self.assertNotContains(response, "Proyecto Oculto")

        response = self.client.get(reverse("projects"), {"tech": "Java"})
        self.assertNotContains(response, "Proyecto Python")

    def test_certifications_render(self):
        Certification.objects.create(
            name="Curso de Python",
            issuer="Udemy",
            year=2024,
            description="Django y Flask.",
        )
        response = self.client.get(reverse("about"))
        self.assertContains(response, "Curso de Python")

    def test_cv_download_returns_pdf(self):
        response = self.client.get(reverse("cv_download"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")
        self.assertIn("attachment", response["Content-Disposition"])
        self.assertIn("CV-test-dev.pdf", response["Content-Disposition"])
        self.assertTrue(response.content.startswith(b"%PDF"))

    def test_custom_404_page(self):
        response = self.client.get("/ruta-que-no-existe/")
        self.assertEqual(response.status_code, 404)
        self.assertContains(response, "Esta ruta no existe", status_code=404)


class ContactFormTests(TestCase):
    def valid_data(self, **overrides):
        data = {
            "name": "Recruiter",
            "email": "recruiter@example.com",
            "company": "Acme",
            "subject": "Oportunidad",
            "message": "Hola, me interesa tu perfil para una posición backend.",
            "website": "",
        }
        data.update(overrides)
        return data

    def test_valid_form(self):
        form = ContactForm(data=self.valid_data())
        self.assertTrue(form.is_valid(), form.errors)

    def test_message_must_have_minimum_length(self):
        form = ContactForm(data=self.valid_data(message="Hola"))
        self.assertFalse(form.is_valid())
        self.assertIn("message", form.errors)

    def test_honeypot_rejects_bots(self):
        form = ContactForm(data=self.valid_data(website="http://spam.example.com"))
        self.assertFalse(form.is_valid())
        self.assertIn("website", form.errors)


class ContactViewTests(TestCase):
    def setUp(self):
        self.url = reverse("contact")
        self.data = {
            "name": "Recruiter",
            "email": "recruiter@example.com",
            "company": "Acme",
            "subject": "Oportunidad",
            "message": "Hola, me interesa tu perfil para una posición backend.",
            "website": "",
        }

    def test_post_creates_message_and_redirects(self):
        response = self.client.post(self.url, self.data)
        self.assertRedirects(response, f"{self.url}#formulario")
        message = ContactMessage.objects.get()
        self.assertEqual(message.name, "Recruiter")
        self.assertEqual(message.ip_address, "127.0.0.1")
        self.assertFalse(message.is_read)

    def test_invalid_post_does_not_create_message(self):
        response = self.client.post(self.url, {**self.data, "message": "Corto"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), 0)

    def test_rate_limit_between_submissions(self):
        self.client.post(self.url, self.data)
        response = self.client.post(
            self.url, {**self.data, "message": "Un segundo mensaje para probar el límite."}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), 1)
        self.assertContains(response, "Esperá unos segundos")
