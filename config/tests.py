from django.core.exceptions import ImproperlyConfigured
from django.test import SimpleTestCase

from .storage import default_storage_config
from .validation import validate_production_config


class StorageConfigTests(SimpleTestCase):
    def test_defaults_to_local_filesystem(self):
        self.assertEqual(
            default_storage_config({}),
            {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        )

    def test_s3_is_opt_in_and_uses_environment_options(self):
        config = default_storage_config(
            {
                "DJANGO_STORAGE_BACKEND": "s3",
                "AWS_STORAGE_BUCKET_NAME": "portfolio-media",
                "AWS_ACCESS_KEY_ID": "access-key",
                "AWS_SECRET_ACCESS_KEY": "secret-key",
                "AWS_S3_REGION_NAME": "auto",
                "AWS_S3_ENDPOINT_URL": "https://s3.example.com",
                "AWS_QUERYSTRING_AUTH": "false",
            }
        )

        self.assertEqual(config["BACKEND"], "storages.backends.s3.S3Storage")
        self.assertEqual(config["OPTIONS"]["bucket_name"], "portfolio-media")
        self.assertEqual(config["OPTIONS"]["access_key"], "access-key")
        self.assertEqual(config["OPTIONS"]["secret_key"], "secret-key")
        self.assertEqual(config["OPTIONS"]["region_name"], "auto")
        self.assertEqual(config["OPTIONS"]["endpoint_url"], "https://s3.example.com")
        self.assertFalse(config["OPTIONS"]["querystring_auth"])
        self.assertFalse(config["OPTIONS"]["file_overwrite"])

    def test_s3_requires_bucket_and_credentials(self):
        with self.assertRaises(ImproperlyConfigured) as error:
            default_storage_config({"DJANGO_STORAGE_BACKEND": "s3"})

        message = str(error.exception)
        self.assertIn("AWS_STORAGE_BUCKET_NAME", message)
        self.assertIn("AWS_ACCESS_KEY_ID", message)
        self.assertIn("AWS_SECRET_ACCESS_KEY", message)


class ProductionConfigTests(SimpleTestCase):
    def valid_env(self, **overrides):
        env = {
            "DJANGO_SECRET_KEY": "x" * 50,
            "DJANGO_ALLOWED_HOSTS": "portfolio.example.com",
            "CONTACT_NOTIFICATION_EMAIL": "",
        }
        env.update(overrides)
        return env

    def assert_valid(self, env, **kwargs):
        validate_production_config(
            env,
            debug=False,
            secret_key=env["DJANGO_SECRET_KEY"],
            allowed_hosts=[env["DJANGO_ALLOWED_HOSTS"]],
            email_backend="django.core.mail.backends.smtp.EmailBackend",
            **kwargs,
        )

    def test_debug_mode_allows_development_defaults(self):
        validate_production_config(
            {},
            debug=True,
            secret_key="django-insecure-portfolio-dev-key-cambiar-en-produccion",
            allowed_hosts=["localhost"],
            email_backend="django.core.mail.backends.console.EmailBackend",
        )

    def test_production_accepts_complete_configuration(self):
        self.assert_valid(self.valid_env())

    def test_production_rejects_development_secret_key(self):
        env = self.valid_env(
            DJANGO_SECRET_KEY="django-insecure-portfolio-dev-key-cambiar-en-produccion"
        )
        with self.assertRaises(ImproperlyConfigured) as error:
            self.assert_valid(env)
        self.assertIn("DJANGO_SECRET_KEY", str(error.exception))

    def test_production_requires_a_public_host(self):
        with self.assertRaises(ImproperlyConfigured) as error:
            validate_production_config(
                self.valid_env(DJANGO_ALLOWED_HOSTS="localhost,127.0.0.1"),
                debug=False,
                secret_key="x" * 50,
                allowed_hosts=["localhost", "127.0.0.1"],
                email_backend="django.core.mail.backends.console.EmailBackend",
            )
        self.assertIn("DJANGO_ALLOWED_HOSTS", str(error.exception))

    def test_render_hostname_is_enough_for_allowed_hosts(self):
        env = self.valid_env(DJANGO_ALLOWED_HOSTS="")
        validate_production_config(
            {**env, "RENDER_EXTERNAL_HOSTNAME": "portfolio.onrender.com"},
            debug=False,
            secret_key="x" * 50,
            allowed_hosts=["localhost", "portfolio.onrender.com"],
            email_backend="django.core.mail.backends.console.EmailBackend",
        )

    def test_notifications_require_smtp_backend(self):
        env = self.valid_env(CONTACT_NOTIFICATION_EMAIL="yo@example.com")
        with self.assertRaises(ImproperlyConfigured) as error:
            validate_production_config(
                env,
                debug=False,
                secret_key="x" * 50,
                allowed_hosts=["portfolio.example.com"],
                email_backend="django.core.mail.backends.console.EmailBackend",
            )
        self.assertIn("EMAIL_BACKEND", str(error.exception))

    def test_smtp_backend_requires_credentials(self):
        env = self.valid_env(CONTACT_NOTIFICATION_EMAIL="yo@example.com")
        with self.assertRaises(ImproperlyConfigured) as error:
            self.assert_valid(env)
        self.assertIn("EMAIL_HOST_PASSWORD", str(error.exception))
