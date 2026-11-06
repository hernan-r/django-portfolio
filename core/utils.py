"""Generación del CV en PDF a partir de los datos cargados en el panel."""

from __future__ import annotations

import re
from io import BytesIO
from urllib.parse import urlsplit
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)
from reportlab.platypus.flowables import Flowable

from .models import Certification, Education, Experience, Profile, Skill

INK = colors.HexColor("#1F2A44")
BODY = colors.HexColor("#374151")
MUTED = colors.HexColor("#4B5563")
RULE = colors.HexColor("#D1D5DB")

MARGIN_X = 17 * mm
MARGIN_TOP = 14 * mm
MARGIN_BOTTOM = 12 * mm

# En el CV "Backend" y "Frontend" se agrupan como "Frameworks".
SKILL_GROUPS = [
    ([Skill.Category.LANGUAGES], "Lenguajes"),
    ([Skill.Category.BACKEND, Skill.Category.FRONTEND], "Frameworks"),
    ([Skill.Category.DATABASE], "Bases de datos"),
    ([Skill.Category.TOOLS], "Herramientas y entornos"),
]


def _styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "name": ParagraphStyle(
            "CVName",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=27,
            leading=31,
            textColor=INK,
            alignment=TA_LEFT,
            spaceAfter=0,
        ),
        "headline": ParagraphStyle(
            "CVHeadline",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=12,
            leading=15,
            textColor=MUTED,
            spaceBefore=4,
        ),
        "contact": ParagraphStyle(
            "CVContact",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9.2,
            leading=14,
            textColor=MUTED,
            spaceBefore=6,
        ),
        "section": ParagraphStyle(
            "CVSection",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=14.5,
            textColor=INK,
            spaceBefore=0,
        ),
        "body": ParagraphStyle(
            "CVBody",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9.4,
            leading=13.8,
            textColor=BODY,
        ),
        "entry": ParagraphStyle(
            "CVEntry",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=10,
            leading=13.5,
            textColor=INK,
            spaceBefore=8,
            spaceAfter=2,
        ),
        "bullet": ParagraphStyle(
            "CVBullet",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9.4,
            leading=13.6,
            textColor=BODY,
            leftIndent=10,
            bulletIndent=0,
            spaceBefore=2.5,
        ),
    }


def _section(title: str, styles: dict[str, ParagraphStyle]) -> list:
    return [
        Spacer(1, 11),
        Paragraph(escape(title), styles["section"]),
        HRFlowable(
            width="100%",
            thickness=0.7,
            color=RULE,
            spaceBefore=2,
            spaceAfter=6,
        ),
    ]


def _paragraphs(text: str, style: ParagraphStyle) -> list:
    blocks = [block.strip() for block in text.split("\n\n") if block.strip()]
    return [Paragraph(escape(block).replace("\n", "<br/>"), style) for block in blocks]


def _bullets(text: str, style: ParagraphStyle) -> list:
    items = [line.strip(" •-\t") for line in text.splitlines() if line.strip()]
    return [Paragraph(escape(item), style, bulletText="•") for item in items]


def _year_range(item: Experience) -> str:
    """Rango de años como en el CV: 2025–2026."""
    start = item.start_date.year
    if item.end_date:
        return f"{start}–{item.end_date.year}"
    if item.is_current:
        return f"{start}–Actualidad"
    # Sin fecha de fin se intenta leer el rango de la fecha personalizada.
    years = re.findall(r"\d{4}", item.date_label or "")
    if len(years) >= 2:
        return f"{years[0]}–{years[1]}"
    return str(start)


def _compact_url(url: str) -> str:
    parts = urlsplit(url)
    host = (parts.netloc or parts.path).removeprefix("www.")
    path = parts.path if parts.netloc else ""
    return f"{host}{path}".rstrip("/")


def _contact_line(profile: Profile) -> str:
    parts = [profile.location, profile.cv_phone, profile.email]
    return "  ·  ".join(escape(part) for part in parts if part)


def _links_line(profile: Profile) -> str:
    links = []
    for url in (
        profile.linkedin_url,
        profile.github_url,
        profile.website_url,
    ):
        if url:
            links.append(
                f"<link href='{escape(url)}' color='#2563EB'>"
                f"{escape(_compact_url(url))}</link>"
            )
    return "  ·  ".join(links)


def _bullet_text(text: str) -> str:
    text = text.strip()
    return text if text.endswith(".") else f"{text}."


def build_cv_pdf(profile: Profile) -> bytes:
    """Construye el PDF del CV y devuelve los bytes."""
    styles = _styles()
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=MARGIN_X,
        rightMargin=MARGIN_X,
        topMargin=MARGIN_TOP,
        bottomMargin=MARGIN_BOTTOM,
        title=profile.full_name,
        author=profile.full_name,
        subject=profile.headline,
        creator="Portfolio Django",
    )

    story: list[Flowable] = []

    # Encabezado
    story.append(Paragraph(escape(profile.full_name), styles["name"]))
    headline = profile.cv_headline or profile.headline
    if headline:
        story.append(Paragraph(escape(headline), styles["headline"]))
    contact = _contact_line(profile)
    if contact:
        story.append(Paragraph(contact, styles["contact"]))
    links = _links_line(profile)
    if links:
        story.append(Paragraph(links, styles["contact"]))

    # Perfil profesional
    summary = profile.cv_summary or profile.short_bio or profile.bio
    if summary:
        story.extend(_section("Perfil profesional", styles))
        story.extend(_paragraphs(summary, styles["body"]))

    # Habilidades técnicas
    skill_lines = []
    for categories, label in SKILL_GROUPS:
        skills: list[Skill] = []
        for category in categories:
            skills.extend(Skill.objects.filter(category=category, show_in_cv=True))
        if skills:
            names = ", ".join(escape(skill.name) for skill in skills)
            skill_lines.append(
                Paragraph(
                    f"<b>{escape(label)}:</b> {names}",
                    styles["body"],
                )
            )
    if skill_lines:
        story.extend(_section("Habilidades técnicas", styles))
        for index, line in enumerate(skill_lines):
            if index:
                story.append(Spacer(1, 1.5))
            story.append(line)

    # Experiencia laboral
    experiences = list(
        Experience.objects.filter(
            kind__in=[Experience.Kind.WORK, Experience.Kind.FREELANCE]
        )
    )
    if experiences:
        story.extend(_section("Experiencia laboral", styles))
        for item in experiences:
            heading = " · ".join(
                part
                for part in (item.role, item.company, _year_range(item))
                if part
            )
            block = [Paragraph(escape(heading), styles["entry"])]
            block.extend(_bullets(item.description, styles["bullet"]))
            story.append(KeepTogether(block))

    # Formación académica
    education = list(Education.objects.all())
    if education:
        story.extend(_section("Formación académica", styles))
        for item in education:
            parts = [f"<b>{escape(item.degree)}</b>"]
            if item.institution:
                parts.append(escape(item.institution))
            if item.date_range:
                parts.append(escape(item.date_range))
            text = " · ".join(parts)
            block = [Paragraph(text, styles["body"])]
            if item.description:
                block.append(Paragraph(escape(item.description), styles["body"]))
            story.append(KeepTogether(block))

    # Cursos y certificaciones
    certifications = list(Certification.objects.all())
    if certifications:
        story.extend(_section("Cursos y certificaciones", styles))
        for item in certifications:
            title = f"{escape(item.issuer)} — {escape(item.name)}"
            if item.year:
                title += f", edición {item.year}"
            if item.description:
                title += f": {escape(item.description)}"
            story.append(
                Paragraph(_bullet_text(title), styles["bullet"], bulletText="•")
            )

    # Habilidades interpersonales
    soft_skills = [
        line.strip(" •-\t")
        for line in (profile.soft_skills or "").splitlines()
        if line.strip()
    ]
    if soft_skills:
        story.extend(_section("Habilidades interpersonales", styles))
        story.append(
            Paragraph(
                escape(" · ".join(soft_skills)) + ".",
                styles["body"],
            )
        )

    # Pie con actualización
    doc.build(story)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf
