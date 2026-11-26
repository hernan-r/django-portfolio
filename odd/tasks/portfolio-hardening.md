# Portfolio hardening: storage, configuración de producción y anti-spam

Objetivo: implementar las mejoras 2 → 1 → 3 propuestas y aceptadas. Rama de trabajo: `feat/portfolio-hardening` (creada desde `main`). Test runner: `.venv/bin/python manage.py test`.

## Specs

### S1 — Las imágenes se pierden en cada deploy
Usuario: "Implementa el orden que mencionaste  2 → 1 → 3, no hagas commit aun solo haz los cambios."
Propuesta aceptada (texto literal): "**2. Las imágenes se pierden en cada deploy** README lo reconoce (`README.md:337-355`) y `render.yaml:30-40` lo deja como comentario. Hoy el avatar y las portadas subidas desde el admin se borran con cada redeploy en Render (filesystem efímero). Es el riesgo operacional más grande del proyecto. → Storage externo (S3-compatible / Cloudinary vía `django-storages`) con `DJANGO_MEDIA_ROOT`/backend por variable de entorno, o disco persistente si pasás a plan pago. Impacto alto, esfuerzo medio."
Alcance autorizado: storage externo S3-compatible configurable por entorno, dependencia, documentación y tests. Sin cambios destructivos en datos existentes.

### S2 — Fallar rápido si falta configuración sensible en producción
Propuesta aceptada (texto literal): "**1. Fallar rápido si falta configuración sensible en producción** `config/settings.py:31-35` usa `django-insecure-portfolio-dev-key-...` como clave por defecto y `DEBUG=True` por defecto. Si en Render no se setea `DJANGO_SECRET_KEY`, el sitio arranca igual con una clave pública. Lo mismo pasa con el email: `EMAIL_BACKEND` cae en consola (`settings.py:183-185`) y las notificaciones se imprimen en logs sin que nadie se entere. → Agregar validación en startup con `ImproperlyConfigured` cuando `DEBUG=False` y falten `SECRET_KEY`/SMTP. Subir `SECURE_HSTS_SECONDS` de `3600` a `31536000` (`settings.py:55`) una vez confirmado HTTPS estable. Ejecutar `manage.py check --deploy` en CI."
Alcance autorizado: validación de configuración productiva, HSTS y documentación. No se agrega CI (no hablado como implementación en este pedido).

### S3 — Anti-spam del formulario es demasiado blando
Propuesta aceptada (texto literal): "**3. Anti-spam del formulario es demasiado blando** El límite es 1 envío cada 30s **por sesión** (`core/views.py:32,184-195`). Un bot rota cookies y sigue insertando filas sin límite. Ya guardás la IP (`models.py:368`) pero no la usás para nada. Además `_notify_contact` usa `fail_silently=True` (`views.py:255`), así que un fallo de SMTP se pierde sin rastro. → Throttle combinado IP + email con ventana deslizante (o `django-ratelimit`), y logging del fallo de email. El honeypot existente (`forms.py:83-87`) se mantiene."
Alcance autorizado: throttle por IP + email, logging del fallo de notificación, tests y documentación. El honeypot y el límite por sesión se conservan.

### Restricción del usuario
"no hagas commit aun solo haz los cambios" — vigente durante la implementación. Luego el usuario autorizó: "prepara el commit ahora con los cambios". Push, PR y merge siguen siendo decisiones del usuario.

## Tasks

- T1 · S1 · inline · storage S3 opcional por entorno + dependencia + docs + tests · GREEN: 27 tests OK (`config.tests`, 3 nuevos) · commit: incluido en el commit de `feat/portfolio-hardening`
- T2 · S2 · inline · validación fail-fast en producción + HSTS + docs + tests · GREEN: 34 tests OK (`config.tests`, 7 nuevos) · commit: incluido en el commit de `feat/portfolio-hardening`
- T3 · S3 · inline · throttle IP/email + logging de email + tests + docs · GREEN: 37 tests OK (`core.tests`, 3 nuevos) · commit: incluido en el commit de `feat/portfolio-hardening`

Decisión de ruta: inline para T1, T2 y T3. No hay Writer trigger: T1 y T2 comparten `config/settings.py` (superposición prohibe escritores paralelos en el mismo árbol) y cada unidad es comprendida y pequeña. Sin verifier independiente: ningún cambio nombra un ítem de alto riesgo de la lista (no hay migraciones de datos, credenciales propias, API pública ni concurrencia nueva).

## Log

L1: "Propone mejoras para el proyecto sin implementar nada aun."
L2: "Implementa el orden que mencionaste  2 → 1 → 3, no hagas commit aun solo haz los cambios."

- 2026-11-26: Exploración inicial completada (settings, views, models, forms, tests, JS, render.yaml). Se confirma que el tema persistente SÍ funciona (`base.html:33-43` + `main.js:32`); no se toca.
- 2026-11-26: API de django-storages verificada en documentación oficial: `STORAGES["default"]["OPTIONS"]` admite `bucket_name`, `access_key`, `secret_key`, `region_name`, `endpoint_url`, `querystring_auth`, `default_acl`, `file_overwrite`.
- 2026-11-26: `.env.example` no es legible con la herramienta de lectura (permission.rejected). No se elude el bloqueo; las variables nuevas se documentan en README.md.
- 2026-11-26: T1 completado. `config/storage.py` decide el backend desde `DJANGO_STORAGE_BACKEND=s3` con fail-fast de bucket/credenciales; `config/settings.py:STORAGES` lo usa; `requirements.txt` agrega `django-storages[s3]>=1.14,<2` (1.14.6 instalada en `.venv`); README y `render.yaml` documentan las variables. RED observado por módulo ausente; GREEN con 27 tests.
- 2026-11-26: T2 completado. `config/validation.py` valida en load de settings: clave secreta no-dev >= 32 chars, host público (o `RENDER_EXTERNAL_HOSTNAME`) y SMTP completo solo si hay `CONTACT_NOTIFICATION_EMAIL`. HSTS 3600 → 31536000. README documenta el fail-fast y `check --deploy`. RED observado por módulo ausente; GREEN con 34 tests. Decisión: no exigir SMTP cuando no hay notificaciones configuradas, para no romper despliegues que guardan mensajes solo en el panel.
- 2026-11-26: T3 completado. `core/views.py` conserva el cooldown por sesión y agrega throttle por IP (60s) y por email (300s) sobre `ContactMessage`; `_notify_contact` usa `fail_silently=False`, captura excepciones y registra el error con `logger`. README actualizado (incluye badge 37 tests). RED: 2 fallos + 1 error; GREEN: 37 tests.
- 2026-11-26: Verificación final: 37 tests OK; backend S3 cargado efectivamente como `storages.backends.s3.S3Storage` con variables de entorno; `DJANGO_DEBUG=False` sin variables produce `ImproperlyConfigured` con mensaje claro. Sin commits: `git status` muestra solo modificaciones y archivos nuevos.
- 2026-11-26: Usuario autorizó el commit: "prepara el commit ahora con los cambios". Se crea la rama `feat/portfolio-hardening` desde `main` y se commitean las tres unidades en un único commit (los archivos `settings.py`, `README.md` y `config/tests.py` son compartidos por las tres unidades, por lo que partirlos en tres commits exigiría reescribir hunks del mismo archivo sin beneficio de revisión). Sin push ni PR.
- 2026-11-26: `.env.example` sigue sin las variables nuevas por restricción de lectura de la herramienta; están documentadas en README y `render.yaml`.
