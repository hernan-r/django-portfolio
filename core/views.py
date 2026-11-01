import ipaddress
import time

from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_GET

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
from .utils import build_cv_pdf

SKILL_CATEGORY_ORDER = [
    Skill.Category.LANGUAGES,
    Skill.Category.BACKEND,
    Skill.Category.DATABASE,
    Skill.Category.TOOLS,
    Skill.Category.FRONTEND,
]

CONTACT_COOLDOWN = 30  # segundos entre envíos por sesión


def _skills_by_category():
    grouped = []
    for category in SKILL_CATEGORY_ORDER:
        skills = list(Skill.objects.filter(category=category))
        if skills:
            grouped.append(
                {
                    "code": category,
                    "label": Skill.Category(category).label,
                    "skills": skills,
                }
            )
    return grouped


def home(request):
    profile = Profile.objects.first()
    featured_projects = Project.objects.filter(is_published=True, is_featured=True)[:3]
    if len(featured_projects) < 3:
        extra = Project.objects.filter(is_published=True).exclude(
            pk__in=[project.pk for project in featured_projects]
        )[: 3 - len(featured_projects)]
        featured_projects = list(featured_projects) + list(extra)

    featured_skills = Skill.objects.filter(is_featured=True).order_by("-level")[:6]
    if not featured_skills:
        featured_skills = Skill.objects.order_by("-level")[:6]

    context = {
        "featured_projects": featured_projects,
        "featured_skills": featured_skills,
        "education": Education.objects.all()[:2],
        "certifications": Certification.objects.all(),
        "work_experience": Experience.objects.filter(
            kind__in=[Experience.Kind.WORK, Experience.Kind.FREELANCE]
        )[:3],
        "stats": {
            "projects": Project.objects.filter(is_published=True).count(),
            "skills": Skill.objects.count(),
            "years": profile.years_experience if profile else 0,
        },
        "meta_title": "Inicio",
        "meta_description": (
            profile.short_bio if profile else "Portfolio de desarrollo backend."
        ),
    }
    return render(request, "core/home.html", context)


def about(request):
    profile = Profile.objects.first()
    context = {
        "education": Education.objects.all(),
        "certifications": Certification.objects.all(),
        "skills_grouped": _skills_by_category(),
        "meta_title": "Sobre mí",
        "meta_description": (
            profile.bio[:160] if profile and profile.bio else "Sobre mí y mi formación."
        ),
    }
    return render(request, "core/about.html", context)


def skills(request):
    context = {
        "skills_grouped": _skills_by_category(),
        "meta_title": "Skills",
        "meta_description": "Tecnologías y herramientas con las que trabajo a diario.",
    }
    return render(request, "core/skills.html", context)


def projects(request):
    q = request.GET.get("q", "").strip()[:100]
    selected_tech = request.GET.get("tech", "").strip()[:60]

    all_projects = list(Project.objects.filter(is_published=True))
    technologies = sorted(
        {tech for project in all_projects for tech in project.technology_list},
        key=str.lower,
    )

    filtered = all_projects
    if q:
        needle = q.lower()
        filtered = [
            project
            for project in filtered
            if needle in project.title.lower()
            or needle in project.short_description.lower()
            or needle in project.description.lower()
            or any(needle in tech.lower() for tech in project.technology_list)
        ]
    if selected_tech:
        filtered = [
            project
            for project in filtered
            if selected_tech.lower()
            in [tech.lower() for tech in project.technology_list]
        ]

    context = {
        "projects": filtered,
        "technologies": technologies,
        "q": q,
        "selected_tech": selected_tech,
        "meta_title": "Proyectos",
        "meta_description": "Proyectos de backend, APIs y aplicaciones que construí.",
    }
    return render(request, "core/projects.html", context)


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug, is_published=True)
    related = (
        Project.objects.filter(is_published=True)
        .exclude(pk=project.pk)
        .order_by("order", "-created_at")[:3]
    )
    context = {
        "project": project,
        "related_projects": related,
        "meta_title": project.title,
        "meta_description": project.short_description,
        "og_image": project.image.url if project.image else None,
    }
    return render(request, "core/project_detail.html", context)


def experience(request):
    context = {
        "work_experience": Experience.objects.filter(
            kind__in=[Experience.Kind.WORK, Experience.Kind.FREELANCE]
        ),
        "personal_experience": Experience.objects.filter(
            kind=Experience.Kind.PERSONAL
        ),
        "education": Education.objects.all(),
        "certifications": Certification.objects.all(),
        "meta_title": "Experiencia",
        "meta_description": "Experiencia laboral y proyectos personales.",
    }
    return render(request, "core/experience.html", context)


def contact(request):
    form = ContactForm(request.POST or None)

    if request.method == "POST":
        last_sent = request.session.get("contact_last_sent", 0)
        if time.time() - last_sent < CONTACT_COOLDOWN:
            form.add_error(
                None,
                "Recibimos tu mensaje hace un momento. Esperá unos segundos antes de enviar otro.",
            )
        elif form.is_valid():
            message = form.save(commit=False)
            message.ip_address = _client_ip(request)
            message.save()
            request.session["contact_last_sent"] = time.time()
            _notify_contact(message)
            messages.success(
                request,
                "¡Mensaje enviado! Gracias por escribirme, te voy a responder a la brevedad.",
            )
            return redirect(f"{reverse('contact')}#formulario")

    context = {
        "form": form,
        "meta_title": "Contacto",
        "meta_description": "Escribime para oportunidades laborales o colaboraciones.",
    }
    return render(request, "core/contact.html", context)


@require_GET
def download_cv(request):
    profile = get_object_or_404(Profile, pk=1)
    pdf = build_cv_pdf(profile)
    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = (
        f'attachment; filename="{profile.cv_pdf_filename}"'
    )
    response["Cache-Control"] = "no-store"
    return response


def _client_ip(request) -> str | None:
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR", "")
    candidates = []
    if forwarded:
        candidates.append(forwarded.split(",")[0].strip())
    candidates.append(request.META.get("REMOTE_ADDR", ""))
    for value in candidates:
        try:
            return str(ipaddress.ip_address(value))
        except ValueError:
            continue
    return None


def _notify_contact(message: ContactMessage) -> None:
    recipient = settings.CONTACT_NOTIFICATION_EMAIL
    if not recipient:
        return
    subject = message.subject or "Nuevo contacto desde el portfolio"
    body = (
        f"Nombre: {message.name}\n"
        f"Email: {message.email}\n"
        f"Empresa: {message.company or '—'}\n"
        f"Asunto: {message.subject or '—'}\n\n"
        f"{message.message}\n"
    )
    email = EmailMessage(
        subject=f"[Portfolio] {subject}",
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[recipient],
        reply_to=[message.email],
    )
    email.send(fail_silently=True)


def handler404(request, exception):
    return render(
        request,
        "404.html",
        {"meta_title": "Página no encontrada"},
        status=404,
    )
