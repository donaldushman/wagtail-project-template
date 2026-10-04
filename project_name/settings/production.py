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

AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = env("AWS_S3_REGION_NAME", default="us-east-2")
AWS_CLOUDFRONT_DOMAIN = env("AWS_CLOUDFRONT_DOMAIN")

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "bucket_name": AWS_STORAGE_BUCKET_NAME,
            "region_name": AWS_S3_REGION_NAME,
            "custom_domain": AWS_CLOUDFRONT_DOMAIN,
            "location": "media",
            "file_overwrite": False,
            "default_acl": None,
            "querystring_auth": False,
        },
    },
    "staticfiles": {
        "BACKEND": "storages.backends.s3.S3ManifestStaticStorage",
        "OPTIONS": {
            "bucket_name": AWS_STORAGE_BUCKET_NAME,
            "region_name": AWS_S3_REGION_NAME,
            "custom_domain": AWS_CLOUDFRONT_DOMAIN,
            "location": "static",
            "default_acl": None,
            "querystring_auth": False,
        },
    },
}

STATIC_URL = f"https://{AWS_CLOUDFRONT_DOMAIN}/static/"
MEDIA_URL = f"https://{AWS_CLOUDFRONT_DOMAIN}/media/"

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
