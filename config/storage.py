"""Selección del backend de almacenamiento de media desde variables de entorno."""

from __future__ import annotations

import os
from collections.abc import Mapping

from django.core.exceptions import ImproperlyConfigured

LOCAL_STORAGE = {"BACKEND": "django.core.files.storage.FileSystemStorage"}
S3_BACKEND = "storages.backends.s3.S3Storage"
TRUTHY_VALUES = {"1", "true", "yes", "on"}


def _env_bool(env: Mapping[str, str], name: str, default: bool = False) -> bool:
    raw = str(env.get(name, "")).strip()
    return raw.lower() in TRUTHY_VALUES if raw else default


def default_storage_config(env: Mapping[str, str] | None = None) -> dict:
    """Devuelve la configuración del storage por defecto.

    El filesystem local sigue siendo el comportamiento por defecto. El backend
    S3-compatible se activa explícitamente con ``DJANGO_STORAGE_BACKEND=s3``,
    lo que permite conservar las imágenes subidas entre deploys en Render.
    """
    env = os.environ if env is None else env

    if str(env.get("DJANGO_STORAGE_BACKEND", "")).strip().lower() != "s3":
        return dict(LOCAL_STORAGE)

    bucket = str(env.get("AWS_STORAGE_BUCKET_NAME", "")).strip()
    access_key = str(env.get("AWS_ACCESS_KEY_ID", "")).strip()
    secret_key = str(env.get("AWS_SECRET_ACCESS_KEY", "")).strip()

    missing = [
        name
        for name, value in (
            ("AWS_STORAGE_BUCKET_NAME", bucket),
            ("AWS_ACCESS_KEY_ID", access_key),
            ("AWS_SECRET_ACCESS_KEY", secret_key),
        )
        if not value
    ]
    if missing:
        raise ImproperlyConfigured(
            "DJANGO_STORAGE_BACKEND=s3 requiere estas variables de entorno: "
            + ", ".join(missing)
        )

    return {
        "BACKEND": S3_BACKEND,
        "OPTIONS": {
            "bucket_name": bucket,
            "access_key": access_key,
            "secret_key": secret_key,
            "region_name": str(env.get("AWS_S3_REGION_NAME", "")).strip() or None,
            "endpoint_url": str(env.get("AWS_S3_ENDPOINT_URL", "")).strip() or None,
            "querystring_auth": _env_bool(env, "AWS_QUERYSTRING_AUTH"),
            "default_acl": None,
            "file_overwrite": False,
        },
    }
