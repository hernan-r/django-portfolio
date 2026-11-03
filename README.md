# Portfolio Backend · Django

Portfolio personal de **Hernán Rosero**, Desarrollador Backend y estudiante de
Ingeniería en Sistemas de Información (UTN).

Sitio construido con **Django 5.2**, HTML, CSS y JavaScript vanilla, con tema
claro/oscuro, diseño responsive, panel de administración y **CV en PDF generado
dinámicamente** desde la base de datos.

![Vista previa del portfolio](docs/screenshots/home-hero-dark.jpg)

<p>
  <img alt="Django" src="https://img.shields.io/badge/Django-5.2-0C4B33?logo=django&logoColor=white">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white">
  <img alt="Tests" src="https://img.shields.io/badge/tests-19%20passing-2ea043">
  <img alt="Licencia" src="https://img.shields.io/badge/licencia-uso%20personal-ef4444">
</p>

---

## Capturas

### Proyectos y experiencia

| Proyectos | Experiencia |
| --- | --- |
| ![Listado de proyectos](docs/screenshots/proyectos.jpg) | ![Experiencia y formación](docs/screenshots/experiencia.jpg) |

### Skills y sobre mí

| Skills | Sobre mí |
| --- | --- |
| ![Skills por categoría](docs/screenshots/skills.jpg) | ![Biografía y formación](docs/screenshots/sobre-mi.jpg) |

### Detalle de proyecto y contacto

| Detalle de proyecto | Contacto |
| --- | --- |
| ![Detalle de Task Tracker CLI](docs/screenshots/proyecto-detalle.jpg) | ![Formulario de contacto](docs/screenshots/contacto.jpg) |

### Tema claro y responsive

| Tema claro | Vista móvil |
| --- | --- |
| ![Inicio con tema claro](docs/screenshots/home-hero-light.jpg) | ![Inicio en móvil](docs/screenshots/home-mobile.jpg) |

> Las capturas fueron tomadas del sitio real en funcionamiento.

---

## Funcionalidades

- **Inicio**: presentación, stack destacado, proyectos y experiencia reciente.
- **Sobre mí**: biografía, perfil profesional, formación académica y cursos.
- **Skills**: habilidades agrupadas por categoría, con nivel y barras animadas.
- **Proyectos**: listado con búsqueda, filtro por tecnología y página de detalle.
- **Experiencia**: trayectoria laboral y formación complementaria en formato timeline.
- **Contacto**: formulario validado con honeypot anti-spam y límite de envíos por sesión.
  Los mensajes quedan guardados en el panel y se puede configurar una notificación por email.
- **CV descargable**: PDF generado al vuelo con perfil, skills, experiencia,
  proyectos, formación y certificaciones.
- **Panel de administración**: perfil único, skills, proyectos, experiencia,
  formación, cursos y bandeja de mensajes.
- **Extras**: tema claro/oscuro persistente, navegación responsive, animaciones al
  hacer scroll, SEO básico, página 404 personalizada y accesibilidad (skip link,
  focus visible, labels, `aria-*`).

## Stack

- Python 3.11 – 3.13 (recomendado 3.11)
- Django 5.2
- PostgreSQL en Render, SQLite en local y MySQL opcional
- Pillow (imágenes de perfil y proyectos)
- ReportLab (CV en PDF)
- WhiteNoise (archivos estáticos en producción)
- HTML, CSS y JavaScript vanilla (sin frameworks de frontend)

### Contenido del portfolio

- **Perfil**: Hernán Rosero · Desarrollador Backend · Rosario, Santa Fe, Argentina.
- **Skills**: Python, Java, SQL; Django, Flask, FastAPI, Spring Boot, Bootstrap;
  MySQL, PostgreSQL; Git, GitHub, Linux/UNIX.
- **Experiencia**: Desarrollador Backend Junior en Deepyze y técnico independiente
  en reparación de PCs y notebooks.
- **Formación**: Ingeniería en Sistemas de Información (UTN, en curso).
- **Cursos**: Udemy, EducaciónIT, Argentina Programa y Código Facilito.
- **Proyectos**:
  - [Task Tracker CLI](https://github.com/hernan-r/task-tracker) — gestor de tareas
    para terminal en Java, sin dependencias externas.
  - [Habit Widget](https://github.com/hernan-r/habit-widget) — app de hábitos para
    iOS 17+ con SwiftUI, SwiftData y widgets interactivos.

---

## Puesta en marcha

```bash
# 1. Crear y activar el entorno virtual
python3.11 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar variables de entorno (opcional en desarrollo)
cp .env.example .env

# 4. Aplicar migraciones (incluye el contenido inicial)
python manage.py migrate

# 5. Crear tu usuario administrador
python manage.py createsuperuser

# 6. Levantar el servidor
python manage.py runserver
```

Abrí:

- Sitio: <http://127.0.0.1:8000/>
- Panel: <http://127.0.0.1:8000/admin/>

> Las migraciones `core/0002_seed_content.py` y `core/0005_real_content.py`
> cargan el contenido inicial basado en el CV. Podés ajustar o reemplazar esos
> datos desde el panel de administración.

---

## Personalizar el portfolio

Ingresá al panel con tu superusuario. Vas a encontrar:

| Sección | Para qué sirve |
| --- | --- |
| **Perfil** | Nombre, titular, foto, biografías, contacto, redes, años de experiencia y resumen del CV. Es un registro único. |
| **Skills** | Nombre, categoría, nivel (0–100), orden y si se destaca en el inicio. |
| **Proyectos** | Título, slug, año, descripciones, tecnologías (separadas por comas), imagen, repo, demo, destacado y publicado. |
| **Experiencia** | Rol, empresa, tipo (laboral/freelance/personal), fechas, viñetas, stack y enlace. |
| **Formación** | Institución, título, fechas, descripción y si está en curso. |
| **Cursos y certificaciones** | Curso, institución, año, descripción y enlace. |
| **Mensajes de contacto** | Bandeja de entrada. Podés marcar como leídos/no leídos. |

### Imágenes

- Foto de perfil: se sube en **Perfil**. Si no hay foto se muestra un monograma.
- Portada de proyecto: se sube en **Proyectos**. Si no hay imagen se genera una
  portada con gradiente y las iniciales del proyecto.
- Los archivos se guardan en `media/` durante el desarrollo.

### CV en PDF

El botón **Descargar CV** apunta a `/cv/`. El PDF se arma en el momento con
ReportLab usando:

- Datos de contacto y resumen del perfil.
- Skills agrupadas por categoría.
- Experiencia laboral y freelance.
- Proyectos publicados.
- Formación académica y cursos/certificaciones.

El archivo se descarga como `CV-hernan-rosero.pdf`. No hay que subir ni actualizar
ningún PDF a mano: cambiás los datos en el panel y el próximo download ya refleja
los cambios.

---

## Contacto y email

Por defecto, Django usa el backend de consola: los emails se imprimen en la
terminal donde corre `runserver`. El mensaje **siempre** queda guardado en
**Mensajes de contacto** del panel.

Para recibir notificaciones reales, configurá en `.env`:

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.tuproveedor.com
EMAIL_PORT=587
EMAIL_HOST_USER=tu-usuario
EMAIL_HOST_PASSWORD=tu-password
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=Portfolio <no-reply@tudominio.com>
CONTACT_NOTIFICATION_EMAIL=tu@email.com
```

El formulario incluye:

- Validación de nombre, email y mensaje (mínimo 20 caracteres).
- Campo honeypot oculto para bots.
- Límite de un envío cada 30 segundos por sesión.
- Guardado de IP para trazabilidad básica.

---

## Base de datos

El proyecto usa SQLite en local y PostgreSQL en Render. La prioridad de
configuración es:

1. `DATABASE_URL` (PostgreSQL).
2. Variables `DB_ENGINE=mysql` (MySQL).
3. SQLite local por defecto.

### PostgreSQL

```env
DATABASE_URL=postgresql://usuario:password@127.0.0.1:5432/portfolio
```

### MySQL (opcional)

Instalá el driver y configurá las variables:

```bash
pip install mysqlclient
```

```env
DB_ENGINE=mysql
DB_NAME=portfolio
DB_USER=root
DB_PASSWORD=tu-password
DB_HOST=127.0.0.1
DB_PORT=3306
```

Después ejecutá `python manage.py migrate`.

---

## Tests

```bash
python manage.py test
```

La suite cubre modelos (singleton del perfil, slugs, iniciales), vistas públicas,
búsqueda/filtros, descarga del PDF, formulario de contacto, honeypot y rate limit.

---

## Estructura

```text
config/                 Configuración y URLs del proyecto
core/
  models.py             Perfil, formación, cursos, skills, proyectos, experiencia, mensajes
  views.py              Vistas públicas y descarga del CV
  forms.py              Formulario de contacto
  admin.py              Panel de administración personalizado
  utils.py              Generación del PDF con ReportLab
  migrations/           Esquema + contenido inicial
  tests.py              Tests automatizados
templates/
  base.html             Layout, navegación, footer y toasts
  core/                 Páginas del sitio
  partials/             Tarjetas, skills, iconos y redes
static/
  css/styles.css        Diseño responsive con tema claro/oscuro
  js/main.js            Tema, menú móvil, animaciones, toasts
docs/
  screenshots/          Capturas usadas en este README
media/                  Imágenes subidas desde el panel
```

### Rutas principales

| Ruta | Vista |
| --- | --- |
| `/` | Inicio |
| `/sobre-mi/` | Sobre mí + formación |
| `/skills/` | Skills por categoría |
| `/proyectos/` | Proyectos con búsqueda y filtros |
| `/proyectos/<slug>/` | Detalle del proyecto |
| `/experiencia/` | Experiencia y formación complementaria |
| `/contacto/` | Formulario de contacto |
| `/cv/` | Descarga del CV en PDF |
| `/admin/` | Panel de administración |

---

## Deploy en Render

El proyecto ya incluye lo necesario para desplegar en Render:

- `render.yaml`: web service + PostgreSQL.
- `build.sh`: instala dependencias, ejecuta `collectstatic` y aplica migraciones.
- `gunicorn` como servidor WSGI.
- Soporte para `DATABASE_URL` (PostgreSQL).
- WhiteNoise para servir los archivos estáticos.
- Configuración automática de `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, HTTPS y cookies seguras cuando `DJANGO_DEBUG=False`.

### Opción 1: Blueprint (recomendado)

1. Subí el repositorio a GitHub.
2. En Render, elegí **New → Blueprint**.
3. Conectá el repositorio y aplicá el blueprint.
4. Render crea automáticamente:
   - El servicio web `django-portfolio`.
   - La base de datos PostgreSQL `portfolio-db`.
   - `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False`, `DATABASE_URL` y `DJANGO_ALLOWED_HOSTS=.onrender.com`.
5. Cuando termine el deploy, creá el superusuario desde **Shell**:

   ```bash
   python manage.py createsuperuser
   ```

6. Abrí `https://<nombre-del-servicio>.onrender.com/` y entrá a `/admin/`.

### Opción 2: configuración manual

Creá un **Web Service** con runtime Python y configurá:

```text
Build Command: ./build.sh
Start Command: gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
```

Después:

1. Creá una base PostgreSQL en Render.
2. Copiá su **Internal Database URL** en la variable `DATABASE_URL` del web service.
3. Agregá estas variables:

| Variable | Valor |
| --- | --- |
| `DJANGO_DEBUG` | `False` |
| `DJANGO_SECRET_KEY` | Una clave nueva y secreta |
| `DJANGO_ALLOWED_HOSTS` | `.onrender.com,tudominio.com` |
| `DATABASE_URL` | Internal Database URL de PostgreSQL |
| `PYTHON_VERSION` | `3.11.9` |

### Archivos subidos (media)

El sistema de archivos de Render es efímero: las imágenes subidas desde el admin
se pierden en cada redeploy. Para conservarlas:

- En planes pagos, agregá un disco persistente en `render.yaml` (hay un ejemplo
  comentado) y definí `DJANGO_MEDIA_ROOT=/var/data/media`.
- O usá un storage externo (S3, Cloudinary, etc.).

### Dominio propio

1. Agregá el dominio en **Settings → Custom Domains** de Render.
2. Sumalo a `DJANGO_ALLOWED_HOSTS`.
3. Agregalo también a `DJANGO_CSRF_TRUSTED_ORIGINS` con el esquema:
   `https://tudominio.com`.

> `build.sh` ejecuta las migraciones en cada deploy. Los datos de PostgreSQL se
> conservan; los archivos de `media/` no, salvo que configures un disco o storage
> externo.

### Otros hostings

El proyecto también funciona con cualquier servidor que soporte Python:

```bash
python manage.py collectstatic --no-input
python manage.py migrate
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

Serví `media/` desde Nginx o un storage externo y configurá HTTPS.

---

## Licencia

Proyecto personal de uso libre. Adaptalo a tu perfil.
