"""Generación del CV en PDF a partir de los datos cargados en el panel."""

from __future__ import annotations

from io import BytesIO
from xml.sax.saxutils import escape

from django.utils import timezone
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
    Table,
    TableStyle,
)

from .models import Certification, Education, Experience, Profile, Project, Skill

INK = colors.HexColor("#0F172A")
BODY = colors.HexColor("#334155")
MUTED = colors.HexColor("#64748B")
ACCENT = colors.HexColor("#047857")
LINE = colors.HexColor("#E2E8F0")

PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN_X = 18 * mm
MARGIN_TOP = 16 * mm
MARGIN_BOTTOM = 17 * mm
CONTENT_WIDTH = PAGE_WIDTH - (MARGIN_X * 2)

SKILL_CATEGORIES = [
    (Skill.Category.LANGUAGES, "Lenguajes"),
    (Skill.Category.BACKEND, "Backend"),
    (Skill.Category.DATABASE, "Bases de datos"),
    (Skill.Category.TOOLS, "Herramientas"),
    (Skill.Category.FRONTEND, "Frontend"),
]


def _styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "name": ParagraphStyle(
            "CVName",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=25,
            leading=28,
            textColor=INK,
            alignment=TA_LEFT,
            spaceAfter=0,
        ),
        "headline": ParagraphStyle(
            "CVHeadline",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=10.5,
            leading=14,
            textColor=ACCENT,
            spaceBefore=3,
        ),
        "contact": ParagraphStyle(
            "CVContact",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8.6,
            leading=12.5,
            textColor=MUTED,
            spaceBefore=5,
        ),
        "section": ParagraphStyle(
            "CVSection",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=9.5,
            leading=12,
            textColor=INK,
            spaceBefore=0,
            spaceAfter=2,
        ),
        "body": ParagraphStyle(
            "CVBody",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9.2,
            leading=13.2,
            textColor=BODY,
        ),
        "small": ParagraphStyle(
            "CVSmall",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8.4,
            leading=12,
            textColor=MUTED,
        ),
        "entry_title": ParagraphStyle(
            "CVEntryTitle",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=10,
            leading=13,
            textColor=INK,
        ),
        "entry_sub": ParagraphStyle(
            "CVEntrySub",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8.8,
            leading=12,
            textColor=ACCENT,
        ),
        "date": ParagraphStyle(
            "CVDate",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8.2,
            leading=11,
            textColor=MUTED,
            alignment=2,
        ),
        "bullet": ParagraphStyle(
            "CVBullet",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=12.6,
            textColor=BODY,
            leftIndent=9,
            bulletIndent=0,
            spaceBefore=1.5,
        ),
        "link": ParagraphStyle(
            "CVLink",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8.4,
            leading=12,
            textColor=ACCENT,
        ),
    }


def _section(title: str, styles: dict[str, ParagraphStyle]) -> list:
    return [
        Spacer(1, 11),
        Paragraph(escape(title.upper()), styles["section"]),
        HRFlowable(
            width="100%",
            thickness=0.8,
            color=LINE,
            spaceBefore=1,
            spaceAfter=7,
        ),
    ]


def _paragraphs(text: str, style: ParagraphStyle) -> list:
    blocks = [block.strip() for block in text.split("\n\n") if block.strip()]
    return [Paragraph(escape(block).replace("\n", "<br/>"), style) for block in blocks]


def _bullets(text: str, style: ParagraphStyle) -> list:
    items = [line.strip(" •-\t") for line in text.splitlines() if line.strip()]
    return [Paragraph(escape(item), style, bulletText="•") for item in items]


def _entry_header(role: str, organization: str, dates: str, styles) -> Table:
    left = [Paragraph(escape(role), styles["entry_title"])]
    if organization:
        left.append(Paragraph(escape(organization), styles["entry_sub"]))
    table = Table(
        [[left, Paragraph(escape(dates), styles["date"])]],
        colWidths=[CONTENT_WIDTH - 34 * mm, 34 * mm],
    )
    table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    return table


def _tech_line(technologies: str, styles) -> Paragraph | None:
    technologies = technologies.strip()
    if not technologies:
        return None
    return Paragraph(
        f"<font color='#047857'><b>Stack:</b></font> {escape(technologies)}",
        styles["small"],
    )


def _contact_line(profile: Profile) -> str:
    parts = [profile.email]
    if profile.phone:
        parts.append(profile.phone)
    if profile.location:
        parts.append(profile.location)
    return "  ·  ".join(escape(part) for part in parts)


def _links_line(profile: Profile) -> str:
    links = []
    for url, label in (
        (profile.github_url, "GitHub"),
        (profile.linkedin_url, "LinkedIn"),
        (profile.website_url, "Sitio web"),
    ):
        if url:
            links.append(f"<link href='{escape(url)}' color='#047857'>{label}</link>")
    return "  ·  ".join(links)


def _footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.6)
    canvas.line(MARGIN_X, 12 * mm, PAGE_WIDTH - MARGIN_X, 12 * mm)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(MARGIN_X, 8 * mm, f"CV · {doc.title}")
    canvas.drawRightString(
        PAGE_WIDTH - MARGIN_X, 8 * mm, f"Página {doc.page}"
    )
    canvas.restoreState()


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

    story: list = []

    # Encabezado
    story.append(Paragraph(escape(profile.full_name), styles["name"]))
    if profile.headline:
        story.append(Paragraph(escape(profile.headline), styles["headline"]))
    story.append(Paragraph(_contact_line(profile), styles["contact"]))
    links = _links_line(profile)
    if links:
        story.append(Paragraph(links, styles["contact"]))
    story.append(
        HRFlowable(
            width="100%", thickness=1.2, color=ACCENT, spaceBefore=9, spaceAfter=2
        )
    )

    # Perfil profesional
    summary = profile.cv_summary or profile.short_bio or profile.bio
    if summary:
        story.extend(_section("Perfil profesional", styles))
        story.extend(_paragraphs(summary, styles["body"]))

    # Habilidades
    skill_lines = []
    for code, label in SKILL_CATEGORIES:
        skills = list(Skill.objects.filter(category=code))
        if skills:
            names = " · ".join(escape(skill.name) for skill in skills)
            skill_lines.append(
                Paragraph(f"<b>{escape(label)}:</b> {names}", styles["body"])
            )
    if skill_lines:
        story.extend(_section("Habilidades técnicas", styles))
        for index, line in enumerate(skill_lines):
            if index:
                story.append(Spacer(1, 2.5))
            story.append(line)

    # Experiencia laboral
    experiences = list(
        Experience.objects.filter(
            kind__in=[Experience.Kind.WORK, Experience.Kind.FREELANCE]
        )
    )
    if experiences:
        story.extend(_section("Experiencia laboral", styles))
        for index, item in enumerate(experiences):
            block = [_entry_header(item.role, item.company, item.date_range, styles)]
            if item.location:
                block.append(Paragraph(escape(item.location), styles["small"]))
            block.extend(_bullets(item.description, styles["bullet"]))
            tech = _tech_line(item.technologies, styles)
            if tech:
                block.append(Spacer(1, 2))
                block.append(tech)
            story.append(KeepTogether(block))
            if index < len(experiences) - 1:
                story.append(Spacer(1, 8))

    # Proyectos
    projects = list(Project.objects.filter(is_published=True))
    if projects:
        story.extend(_section("Proyectos destacados", styles))
        for index, project in enumerate(projects):
            links = []
            if project.repository_url:
                links.append(
                    f"<link href='{escape(project.repository_url)}' color='#047857'>Repositorio</link>"
                )
            if project.demo_url:
                links.append(
                    f"<link href='{escape(project.demo_url)}' color='#047857'>Demo</link>"
                )
            block = [
                _entry_header(
                    project.title,
                    " · ".join(project.technology_list),
                    str(project.year),
                    styles,
                ),
                Spacer(1, 2),
                Paragraph(escape(project.short_description), styles["body"]),
            ]
            if links:
                block.append(Paragraph(" · ".join(links), styles["link"]))
            story.append(KeepTogether(block))
            if index < len(projects) - 1:
                story.append(Spacer(1, 7))

    # Formación
    education = list(Education.objects.all())
    if education:
        story.extend(_section("Formación académica", styles))
        for index, item in enumerate(education):
            block = [
                _entry_header(
                    item.degree,
                    item.institution,
                    item.date_range,
                    styles,
                )
            ]
            if item.description:
                block.append(
                    Paragraph(escape(item.description), styles["small"])
                )
            story.append(KeepTogether(block))
            if index < len(education) - 1:
                story.append(Spacer(1, 6))

    # Cursos y certificaciones
    certifications = list(Certification.objects.all())
    if certifications:
        story.extend(_section("Cursos y certificaciones", styles))
        for index, item in enumerate(certifications):
            block = [
                _entry_header(
                    item.name,
                    item.issuer,
                    item.date_label,
                    styles,
                )
            ]
            if item.description:
                block.append(Paragraph(escape(item.description), styles["small"]))
            story.append(KeepTogether(block))
            if index < len(certifications) - 1:
                story.append(Spacer(1, 6))

    # Pie con actualización
    story.append(Spacer(1, 14))
    story.append(
        Paragraph(
            f"Actualizado en {timezone.localdate().strftime('%m/%Y')}",
            styles["small"],
        )
    )

    doc.build(story, onFirstPage=_footer, onLaterPages=_footer)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf
