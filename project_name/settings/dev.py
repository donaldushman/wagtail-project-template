import environ

from .base import *


env = environ.Env()
environ.Env.read_env(BASE_DIR / ".env")

DEBUG = True
SECRET_KEY = env("SECRET_KEY", default="dev-only-secret-key")
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "[::1]"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DATABASE_NAME", default="{{ project_name }}"),
        "USER": env("DATABASE_USER", default="postgres"),
        "PASSWORD": env("DATABASE_PASSWORD", default=""),
        "HOST": env("DATABASE_HOST", default="localhost"),
        "PORT": env("DATABASE_PORT", default="5432"),
    }
}

STATIC_ROOT = BASE_DIR / "static"
MEDIA_ROOT = BASE_DIR / "media"
SITE_URL = env("SITE_URL", default="http://localhost:8000")
BASE_URL = SITE_URL
WAGTAILADMIN_BASE_URL = SITE_URL
