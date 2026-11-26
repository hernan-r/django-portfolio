"""Validación de la configuración mínima requerida en producción."""

from __future__ import annotations

from collections.abc import Mapping

from django.core.exceptions import ImproperlyConfigured

DEV_SECRET_KEY = "django-insecure-portfolio-dev-key-cambiar-en-produccion"
LOCAL_HOSTS = {"localhost", "127.0.0.1", "[::1]"}


def validate_production_config(
    env: Mapping[str, str],
    *,
    debug: bool,
    secret_key: str,
    allowed_hosts: list[str],
    email_backend: str,
) -> None:
    """Falla temprano si el despliegue no tiene la configuración segura mínima.

    Se llama al cargar ``config.settings`` para que gunicorn no arranque con la
    clave de desarrollo, con hosts locales o con notificaciones silenciosas.
    """
    if debug:
        return

    problems: list[str] = []
    key = str(secret_key or "").strip()
    if not key or key == DEV_SECRET_KEY or len(key) < 32:
        problems.append(
            "DJANGO_SECRET_KEY debe estar definida, ser única y tener al menos 32 caracteres"
        )

    has_public_host = any(host not in LOCAL_HOSTS for host in allowed_hosts)
    render_host = str(env.get("RENDER_EXTERNAL_HOSTNAME", "")).strip()
    if not has_public_host and not render_host:
        problems.append(
            "DJANGO_ALLOWED_HOSTS debe incluir el host público "
            "(o RENDER_EXTERNAL_HOSTNAME cuando se despliega en Render)"
        )

    notification = str(env.get("CONTACT_NOTIFICATION_EMAIL", "")).strip()
    if notification:
        if "smtp" not in email_backend.lower():
            problems.append(
                "EMAIL_BACKEND debe ser SMTP cuando CONTACT_NOTIFICATION_EMAIL está configurado"
            )
        else:
            for name in ("EMAIL_HOST", "EMAIL_HOST_USER", "EMAIL_HOST_PASSWORD"):
                if not str(env.get(name, "")).strip():
                    problems.append(f"{name} es requerido para enviar notificaciones")

    if problems:
        raise ImproperlyConfigured(
            "Configuración de producción inválida:\n- " + "\n- ".join(problems)
        )
