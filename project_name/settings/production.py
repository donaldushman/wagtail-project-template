from urllib.parse import urlparse

import dj_database_url
import environ

from .base import *


env = environ.Env()

DEBUG = False

SECRET_KEY = env("SECRET_KEY")
SITE_URL = env("SITE_URL").rstrip("/")

site = urlparse(SITE_URL)
if not site.hostname:
    raise ValueError("SITE_URL must include a valid hostname.")

ALLOWED_HOSTS = env.list(
    "ALLOWED_HOSTS",
    default=[site.hostname, f"www.{site.hostname}"],
)

CSRF_TRUSTED_ORIGINS = env.list(
    "CSRF_TRUSTED_ORIGINS",
    default=[SITE_URL],
)

DATABASES = {
    "default": dj_database_url.config(
        default=env("DATABASE_URL"),
        conn_max_age=600,
        conn_health_checks=True,
        ssl_require=True,
    )
}

BASE_URL = SITE_URL
WAGTAILADMIN_BASE_URL = SITE_URL

STATIC_ROOT = BASE_DIR / "staticfiles"

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
