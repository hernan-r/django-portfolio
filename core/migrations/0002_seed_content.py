import datetime

from django.db import migrations


def seed_content(apps, schema_editor):
    Profile = apps.get_model("core", "Profile")
    Education = apps.get_model("core", "Education")
    Skill = apps.get_model("core", "Skill")
    Project = apps.get_model("core", "Project")
    Experience = apps.get_model("core", "Experience")

    Profile.objects.update_or_create(
        pk=1,
        defaults={
            "full_name": "Hernán",
            "headline": "Backend Developer · Python, Django & FastAPI",
            "tagline": (
                "Diseño y construyo APIs robustas, escalables y bien documentadas. "
                "Me especializo en Python, Django y FastAPI, con foco en arquitecturas "
                "limpias y datos eficientes."
            ),
            "short_bio": (
                "Desarrollador backend con experiencia construyendo APIs y sistemas de "
                "gestión. Estudiante de Ingeniería en Sistemas en la UTN, con foco en "
                "Python, Django, FastAPI y bases de datos relacionales."
            ),
            "bio": (
                "Empecé a programar en la facultad y encontré en el backend el lugar donde "
                "todo lo que me gusta se cruza: lógica, datos, arquitectura y resolver "
                "problemas concretos. Desde entonces no paré de construir proyectos y de "
                "aprender de cada uno.\n\n"
                "Actualmente estudio Ingeniería en Sistemas de Información en la "
                "Universidad Tecnológica Nacional (UTN) y trabajo como Backend Developer "
                "en productos SaaS, desarrollando APIs con Python, Django y FastAPI. "
                "También tengo experiencia con Java y Spring Boot, lo que me permite "
                "moverme con comodidad entre distintos ecosistemas.\n\n"
                "Me interesa escribir código que otra persona pueda entender, con tests que "
                "den confianza y decisiones técnicas que se sostengan en el tiempo. Creo "
                "que un buen backend no se ve: simplemente funciona, escala y no despierta "
                "a nadie a las tres de la mañana."
            ),
            "cv_summary": (
                "Backend Developer con experiencia en el diseño y desarrollo de APIs REST, "
                "modelado de datos y despliegue de aplicaciones. Manejo de Python, Django, "
                "Django REST Framework, FastAPI, Java, Spring Boot, MySQL y Git. Estudiante "
                "de Ingeniería en Sistemas de Información en la UTN, orientado a código "
                "limpio, testing y mejora continua."
            ),
            "email": "hernan@example.com",
            "phone": "",
            "location": "Buenos Aires, Argentina",
            "availability": "Disponible para nuevas oportunidades",
            "github_url": "https://github.com/herndev",
            "linkedin_url": "https://www.linkedin.com/in/herndev",
            "years_experience": 5,
        },
    )

    education = [
        {
            "institution": "Universidad Tecnológica Nacional (UTN)",
            "degree": "Ingeniería en Sistemas de Información",
            "start_date": datetime.date(2021, 3, 1),
            "end_date": None,
            "is_current": True,
            "description": (
                "Carrera de grado con foco en algoritmos, arquitectura de software, bases "
                "de datos y gestión de proyectos. Participación en proyectos integradores "
                "y ayudantía en materias de programación."
            ),
            "order": 0,
        },
        {
            "institution": "Universidad Tecnológica Nacional (UTN)",
            "degree": "Tecnicatura Universitaria en Programación",
            "start_date": datetime.date(2019, 3, 1),
            "end_date": datetime.date(2021, 12, 1),
            "is_current": False,
            "description": (
                "Formación técnica en desarrollo de software, estructuras de datos y bases "
                "de datos. Trabajo final: sistema de gestión de turnos con Django y MySQL."
            ),
            "order": 1,
        },
    ]
    for item in education:
        Education.objects.update_or_create(
            degree=item["degree"], defaults=item
        )

    skills = [
        # Lenguajes
        ("Python", "languages", 92, 1, True),
        ("Java", "languages", 80, 2, True),
        ("SQL", "languages", 86, 3, False),
        # Backend
        ("Django", "backend", 92, 1, True),
        ("Django REST Framework", "backend", 88, 2, False),
        ("FastAPI", "backend", 86, 3, True),
        ("Spring Boot", "backend", 78, 4, False),
        ("APIs REST", "backend", 90, 5, False),
        # Bases de datos
        ("MySQL", "database", 88, 1, True),
        ("PostgreSQL", "database", 78, 2, False),
        ("Redis", "database", 64, 3, False),
        # Herramientas
        ("Git", "tools", 90, 1, True),
        ("Docker", "tools", 76, 2, False),
        ("Linux", "tools", 72, 3, False),
        ("GitHub Actions", "tools", 68, 4, False),
        # Frontend
        ("HTML & CSS", "frontend", 76, 1, False),
        ("JavaScript", "frontend", 66, 2, False),
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

    projects = [
        {
            "title": "API de Gestión de Turnos",
            "slug": "api-de-gestion-de-turnos",
            "short_description": (
                "API REST para reservar, reprogramar y administrar turnos, con "
                "autenticación JWT, roles y notificaciones por email."
            ),
            "description": (
                "Sistema backend para clínicas y consultorios que necesitaban reemplazar "
                "una agenda en planillas por un flujo de reservas confiable.\n\n"
                "La API permite a los pacientes consultar disponibilidad y reservar turnos, "
                "mientras que el personal administrativo gestiona profesionales, horarios y "
                "cancelaciones desde un panel. Implementé autenticación con JWT, permisos "
                "por rol y validaciones de solapamiento a nivel de base de datos para evitar "
                "doble reserva.\n\n"
                "El proyecto incluye tests de integración con Pytest, documentación OpenAPI "
                "y un Dockerfile para levantar la aplicación junto a MySQL en un solo paso."
            ),
            "technologies": "Python, Django, Django REST Framework, MySQL, JWT, Docker",
            "repository_url": "https://github.com/herndev/turnos-api",
            "demo_url": "https://turnos.hernandev.dev",
            "is_featured": True,
            "order": 1,
        },
        {
            "title": "Marketplace API",
            "slug": "marketplace-api",
            "short_description": (
                "Backend de un marketplace con catálogo, carrito, órdenes y pagos, "
                "construido con FastAPI, PostgreSQL y Redis."
            ),
            "description": (
                "API de alto rendimiento para un marketplace de productos artesanales. "
                "Modela vendedores, publicaciones, variantes, stock, carrito y órdenes, con "
                "un flujo de pago simulado y webhooks para actualizar el estado de cada "
                "compra.\n\n"
                "Usé FastAPI y Pydantic para validación y documentación automática, "
                "PostgreSQL para la persistencia y Redis como caché de catálogo y "
                "almacenamiento de sesiones. La arquitectura separa routers, servicios y "
                "repositorios para facilitar el testing.\n\n"
                "Incluye migraciones con Alembic, tests con Pytest y un entorno completo con "
                "Docker Compose."
            ),
            "technologies": "Python, FastAPI, PostgreSQL, Redis, SQLAlchemy, Docker",
            "repository_url": "https://github.com/herndev/marketplace-api",
            "demo_url": "https://marketplace-api.hernandev.dev/docs",
            "is_featured": True,
            "order": 2,
        },
        {
            "title": "Sistema de Facturación",
            "slug": "sistema-de-facturacion",
            "short_description": (
                "Aplicación de facturación para PyMEs con clientes, comprobantes, "
                "reportes y control de stock, desarrollada en Java y Spring Boot."
            ),
            "description": (
                "Aplicación web pensada para pequeños comercios que necesitaban emitir "
                "comprobantes y llevar control de stock sin depender de un software de "
                "escritorio. El backend está desarrollado con Java y Spring Boot, con "
                "Spring Security para autenticación y Spring Data JPA para la persistencia "
                "en MySQL.\n\n"
                "El sistema permite administrar clientes, productos, comprobantes y pagos, "
                "además de generar reportes de ventas por período. La interfaz se resolvió "
                "con Thymeleaf y Bootstrap, manteniendo el foco en el flujo de negocio.\n\n"
                "Fue mi primer proyecto grande en el ecosistema Java y me sirvió para "
                "profundizar en transacciones, validación y diseño de capas."
            ),
            "technologies": "Java, Spring Boot, MySQL, Spring Security, JPA, Thymeleaf",
            "repository_url": "https://github.com/herndev/facturacion-spring",
            "demo_url": "",
            "is_featured": True,
            "order": 3,
        },
        {
            "title": "Panel de Métricas Internas",
            "slug": "panel-de-metricas-internas",
            "short_description": (
                "Dashboard para visualizar métricas de producto y operaciones, con "
                "consultas agregadas y exportación de reportes."
            ),
            "description": (
                "Herramienta interna para centralizar métricas dispersas en distintas "
                "planillas. El backend consolida datos de ventas, soporte y uso del producto, "
                "y expone endpoints agregados por período para alimentar el dashboard.\n\n"
                "Implementé tareas programadas para sincronizar información, caché de "
                "consultas pesadas y una capa de permisos para que cada área vea solo los "
                "datos que le corresponden.\n\n"
                "El frontend del panel se construyó con Django Templates y Chart.js, "
                "priorizando claridad y velocidad de carga."
            ),
            "technologies": "Python, Django, PostgreSQL, Chart.js, Celery, Redis",
            "repository_url": "https://github.com/herndev/metricas-panel",
            "demo_url": "",
            "is_featured": False,
            "order": 4,
        },
    ]
    for item in projects:
        Project.objects.update_or_create(title=item["title"], defaults=item)

    experiences = [
        {
            "role": "Backend Developer",
            "company": "Estudio Digital Andina",
            "kind": "work",
            "location": "Buenos Aires · Híbrido",
            "start_date": datetime.date(2024, 2, 1),
            "end_date": None,
            "is_current": True,
            "description": (
                "Desarrollo y mantenimiento de APIs REST con Django y Django REST "
                "Framework para productos SaaS.\n"
                "Diseño de modelos y migraciones sobre MySQL, optimizando consultas "
                "críticas y reduciendo tiempos de respuesta.\n"
                "Implementación de autenticación con JWT, permisos por rol y "
                "documentación OpenAPI para equipos externos.\n"
                "Participación en revisiones de código, definición de estándares y "
                "acompañamiento de desarrolladores junior."
            ),
            "technologies": "Python, Django, DRF, MySQL, Docker, Git",
            "url": "",
            "order": 0,
        },
        {
            "role": "Backend Developer Jr.",
            "company": "Tecnología Sur S.A.",
            "kind": "work",
            "location": "Buenos Aires · Presencial",
            "start_date": datetime.date(2022, 8, 1),
            "end_date": datetime.date(2024, 1, 31),
            "is_current": False,
            "description": (
                "Desarrollo de servicios internos con Java y Spring Boot para el área "
                "de operaciones.\n"
                "Migración de procesos manuales a endpoints REST con validación y "
                "trazabilidad.\n"
                "Escritura de tests unitarios y documentación técnica de los módulos "
                "implementados.\n"
                "Trabajo conjunto con el equipo de datos para integrar reportes en MySQL."
            ),
            "technologies": "Java, Spring Boot, MySQL, Maven, Git",
            "url": "",
            "order": 1,
        },
        {
            "role": "Desarrollador Backend Freelance",
            "company": "Proyectos independientes",
            "kind": "freelance",
            "location": "Remoto",
            "start_date": datetime.date(2021, 6, 1),
            "end_date": datetime.date(2022, 7, 31),
            "is_current": False,
            "description": (
                "Desarrollo de sitios y APIs a medida para pequeños negocios y "
                "profesionales independientes.\n"
                "Relevamiento de requerimientos, definición de alcance y entrega con "
                "documentación de uso.\n"
                "Implementación de formularios, paneles de administración y despliegues "
                "en servidores Linux."
            ),
            "technologies": "Python, Django, MySQL, HTML, CSS, Linux",
            "url": "",
            "order": 2,
        },
        {
            "role": "Desarrollo backend y modelo de datos",
            "company": "API de Gestión de Turnos",
            "kind": "personal",
            "location": "Proyecto personal",
            "start_date": datetime.date(2024, 3, 1),
            "end_date": None,
            "is_current": True,
            "description": (
                "Diseñé la API y el modelo de datos para evitar reservas duplicadas, "
                "con autenticación JWT y permisos por rol.\n"
                "Escribí tests de integración y documenté los endpoints con OpenAPI."
            ),
            "technologies": "Python, Django, DRF, MySQL, Docker",
            "url": "https://github.com/herndev/turnos-api",
            "order": 0,
        },
        {
            "role": "Automatización de procesos",
            "company": "Scripts & tooling",
            "kind": "personal",
            "location": "Proyecto personal",
            "start_date": datetime.date(2023, 1, 1),
            "end_date": datetime.date(2023, 12, 1),
            "is_current": False,
            "description": (
                "Construí scripts en Python para ordenar, validar y consolidar planillas "
                "de distintos orígenes.\n"
                "Expuse los resultados con una pequeña API en FastAPI y los automaticé "
                "con tareas programadas."
            ),
            "technologies": "Python, FastAPI, Pandas, SQLite",
            "url": "https://github.com/herndev/automatizaciones",
            "order": 1,
        },
    ]
    for item in experiences:
        Experience.objects.update_or_create(
            role=item["role"], company=item["company"], defaults=item
        )


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_content, migrations.RunPython.noop),
    ]
