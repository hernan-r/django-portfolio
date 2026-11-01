import datetime

from django.db import migrations


def seed_real_content(apps, schema_editor):
    Profile = apps.get_model("core", "Profile")
    Education = apps.get_model("core", "Education")
    Certification = apps.get_model("core", "Certification")
    Skill = apps.get_model("core", "Skill")
    Project = apps.get_model("core", "Project")
    Experience = apps.get_model("core", "Experience")

    # Perfil
    Profile.objects.update_or_create(
        pk=1,
        defaults={
            "full_name": "Hernán Rosero",
            "headline": "Desarrollador Backend · Python, Django & Java",
            "tagline": (
                "Desarrollador Backend y estudiante de Ingeniería en Sistemas de "
                "Información (UTN). Construyo APIs REST y aplicaciones con Python, "
                "Django, Flask, FastAPI y Java con Spring Boot."
            ),
            "short_bio": (
                "Desarrollador Backend y estudiante de Ingeniería en Sistemas de "
                "Información (UTN), con formación práctica en Python (Django, Flask y "
                "FastAPI) y Java (Spring Boot). Conocimientos de APIs REST, "
                "operaciones CRUD y bases de datos relacionales como MySQL y "
                "PostgreSQL."
            ),
            "bio": (
                "Soy desarrollador backend y estudiante de Ingeniería en Sistemas de "
                "Información en la Universidad Tecnológica Nacional (UTN). Me formé de "
                "manera práctica en Python, con Django, Flask y FastAPI, y en Java con "
                "Spring Boot.\n\n"
                "Trabajo con APIs REST, operaciones CRUD y bases de datos "
                "relacionales como MySQL y PostgreSQL. Uso Git y GitHub para el control "
                "de versiones, la revisión de cambios y el trabajo colaborativo.\n\n"
                "Antes de mi rol actual me desempeñé como técnico independiente en "
                "reparación de PCs y notebooks. Esa etapa me dio un enfoque metódico "
                "para resolver problemas, aprender continuamente y trabajar en equipo."
            ),
            "cv_summary": (
                "Desarrollador Backend y estudiante de Ingeniería en Sistemas de "
                "Información (UTN), con formación práctica en Python (Django, Flask y "
                "FastAPI) y Java (Spring Boot). Conocimientos de APIs REST, "
                "operaciones CRUD y bases de datos relacionales como MySQL y "
                "PostgreSQL. Experiencia previa en soporte técnico y atención a "
                "clientes, con enfoque metódico para resolver problemas, aprender "
                "continuamente y trabajar en equipo."
            ),
            "email": "agusrosero2000@gmail.com",
            "phone": "",
            "location": "Rosario, Santa Fe, Argentina",
            "availability": "Abierto a nuevas oportunidades",
            "github_url": "https://github.com/hernan-r",
            "linkedin_url": "https://www.linkedin.com/in/hernan-rosero",
            "twitter_url": "",
            "website_url": "",
            "years_experience": 2,
        },
    )

    # Eliminar datos de demostración que ya no corresponden.
    Education.objects.filter(degree="Tecnicatura Universitaria en Programación").delete()
    Skill.objects.filter(
        name__in=[
            "Django REST Framework",
            "APIs REST",
            "Redis",
            "HTML & CSS",
            "JavaScript",
            "Docker",
            "GitHub Actions",
            "Linux",
        ]
    ).delete()
    for slug in [
        "api-de-gestion-de-turnos",
        "marketplace-api",
        "sistema-de-facturacion",
        "panel-de-metricas-internas",
    ]:
        Project.objects.filter(slug=slug).delete()
    for role, company in [
        ("Backend Developer", "Estudio Digital Andina"),
        ("Backend Developer Jr.", "Tecnología Sur S.A."),
        ("Desarrollador Backend Freelance", "Proyectos independientes"),
        ("Desarrollo backend y modelo de datos", "API de Gestión de Turnos"),
        ("Automatización de procesos", "Scripts & tooling"),
    ]:
        Experience.objects.filter(role=role, company=company).delete()

    # Formación académica
    Education.objects.update_or_create(
        degree="Ingeniería en Sistemas de Información",
        defaults={
            "institution": "Universidad Tecnológica Nacional (UTN)",
            "start_date": None,
            "end_date": None,
            "is_current": True,
            "description": "",
            "order": 0,
        },
    )

    # Cursos y certificaciones
    certifications = [
        {
            "name": "Universidad Python (+71 h)",
            "issuer": "Udemy",
            "year": None,
            "description": "Django, Flask y proyectos web integrados con PostgreSQL.",
            "order": 1,
        },
        {
            "name": "Python para Profesionales",
            "issuer": "Udemy",
            "year": None,
            "description": "Buenas prácticas y optimización de código.",
            "order": 2,
        },
        {
            "name": "Git",
            "issuer": "Udemy",
            "year": None,
            "description": "Control de versiones.",
            "order": 3,
        },
        {
            "name": "Bases de Datos y Web",
            "issuer": "EducaciónIT",
            "year": None,
            "description": "SQL, fundamentos de bases de datos y JavaScript.",
            "order": 4,
        },
        {
            "name": "Primera Etapa",
            "issuer": "Argentina Programa",
            "year": 2022,
            "description": "",
            "order": 5,
        },
        {
            "name": "Curso a fondo de GitHub",
            "issuer": "Código Facilito",
            "year": None,
            "description": "Repositorios y flujos de trabajo colaborativos.",
            "order": 6,
        },
    ]
    for item in certifications:
        Certification.objects.update_or_create(
            name=item["name"], issuer=item["issuer"], defaults=item
        )

    # Skills
    skills = [
        ("Python", "languages", 85, 1, True),
        ("Java", "languages", 75, 2, True),
        ("SQL", "languages", 80, 3, False),
        ("Django", "backend", 85, 1, True),
        ("Flask", "backend", 75, 2, False),
        ("FastAPI", "backend", 75, 3, True),
        ("Spring Boot", "backend", 70, 4, False),
        ("APIs REST", "backend", 80, 5, False),
        ("MySQL", "database", 80, 1, True),
        ("PostgreSQL", "database", 75, 2, False),
        ("Git", "tools", 85, 1, True),
        ("GitHub", "tools", 85, 2, False),
        ("Linux/UNIX", "tools", 70, 3, False),
        ("Bootstrap", "frontend", 70, 1, False),
    ]
    for name, category, level, order, featured in skills:
        Skill.objects.update_or_create(
            name=name,
            defaults={
                "category": category,
                "level": level,
                "order": order,
                "is_featured": featured,
            },
        )

    # Proyectos reales de GitHub
    projects = [
        {
            "title": "Task Tracker CLI",
            "slug": "task-tracker-cli",
            "year": 2026,
            "short_description": (
                "Gestor de tareas para terminal escrito en Java, sin dependencias "
                "externas, con persistencia TSV, filtros y barra de progreso."
            ),
            "description": (
                "Gestor de tareas para terminal escrito en Java, pensado para "
                "funcionar solo con el JDK. Se compila con `javac` y se ejecuta "
                "como un único jar, sin dependencias externas.\n\n"
                "Incluye los comandos `add`, `list`, `done` y `delete`, con "
                "soporte para varios IDs y filtros por pendientes, completadas o "
                "todas. Cada listado muestra una tabla alineada y una barra de "
                "progreso con el porcentaje global; los colores se activan solo "
                "en terminales y respetan `NO_COLOR`.\n\n"
                "Las tareas se guardan en un archivo TSV en UTF-8 con escritura "
                "atómica, compatible con edición manual. El CLI valida IDs, "
                "argumentos y archivos corruptos, y devuelve códigos de salida "
                "distintos para errores de uso y de almacenamiento. El proyecto "
                "incluye pruebas de integración con `./test.sh`."
            ),
            "technologies": "Java, CLI, TSV, Git",
            "repository_url": "https://github.com/hernan-r/task-tracker",
            "demo_url": "",
            "is_featured": True,
            "order": 1,
        },
        {
            "title": "Habit Widget",
            "slug": "habit-widget",
            "year": 2026,
            "short_description": (
                "App de hábitos para iOS 17+ con widgets interactivos, SwiftUI, "
                "SwiftData, gráficos y notificaciones locales."
            ),
            "description": (
                "App de seguimiento de hábitos para iPhone y iPad desarrollada con "
                "SwiftUI y SwiftData. Permite crear hábitos con ícono, categoría y "
                "frecuencia, calcular rachas, ver el progreso diario y consultar "
                "estadísticas con Swift Charts y un heatmap de los últimos 28 "
                "días.\n\n"
                "Incluye widgets interactivos para pantalla de inicio y pantalla "
                "de bloqueo, configurables por categoría mediante App Intents y "
                "con la posibilidad de marcar hábitos sin abrir la app. También "
                "programa recordatorios locales por hábito y permite exportar e "
                "importar los datos en JSON.\n\n"
                "El proyecto usa únicamente frameworks de Apple, sin dependencias "
                "externas, con SwiftData compartido entre la app y la extensión "
                "mediante un App Group, y pruebas de la lógica de completado con "
                "XCTest."
            ),
            "technologies": "Swift, SwiftUI, SwiftData, WidgetKit, Swift Charts, iOS",
            "repository_url": "https://github.com/hernan-r/habit-widget",
            "demo_url": "",
            "is_featured": True,
            "order": 2,
        },
    ]
    for item in projects:
        Project.objects.update_or_create(slug=item["slug"], defaults=item)

    # Experiencia laboral
    experiences = [
        {
            "role": "Desarrollador Backend Junior",
            "company": "Deepyze",
            "kind": "work",
            "location": "",
            "start_date": datetime.date(2025, 1, 1),
            "end_date": None,
            "is_current": True,
            "description": (
                "Desarrollo y mantenimiento de endpoints para APIs REST utilizando "
                "Python y frameworks como Django, Flask o FastAPI.\n"
                "Implementación de operaciones CRUD e integración con bases de "
                "datos relacionales MySQL y PostgreSQL.\n"
                "Colaboración en el desarrollo de servicios backend con Java y "
                "Spring Boot, aplicando una estructura por capas.\n"
                "Uso de Git y GitHub para control de versiones, revisión de "
                "cambios y trabajo colaborativo.\n"
                "Depuración de errores, pruebas funcionales y documentación "
                "técnica de funcionalidades."
            ),
            "technologies": (
                "Python, Django, Flask, FastAPI, Java, Spring Boot, MySQL, "
                "PostgreSQL, Git, GitHub"
            ),
            "url": "",
            "order": 0,
        },
        {
            "role": "Técnico en reparación de PCs y notebooks",
            "company": "Autónomo",
            "kind": "freelance",
            "location": "",
            "start_date": datetime.date(2021, 1, 1),
            "end_date": datetime.date(2023, 12, 31),
            "is_current": False,
            "description": (
                "Configuré y desplegué distribuciones Linux/UNIX y sistemas "
                "Windows, optimizando el rendimiento de equipos.\n"
                "Realicé copias de seguridad y recuperación de información, "
                "priorizando la integridad de los datos.\n"
                "Resolví incidencias de hardware y software para mejorar la "
                "estabilidad operativa de los equipos.\n"
                "Atendí directamente a clientes, relevé necesidades, comuniqué "
                "diagnósticos y cumplí plazos acordados."
            ),
            "technologies": "Linux/UNIX, Windows, Hardware, Software, Backups",
            "url": "",
            "order": 1,
        },
    ]
    for item in experiences:
        Experience.objects.update_or_create(
            role=item["role"], company=item["company"], defaults=item
        )


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0004_certification_alter_education_start_date"),
    ]

    operations = [
        migrations.RunPython(seed_real_content, migrations.RunPython.noop),
    ]