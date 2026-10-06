Architecture
============

The project is a Django and Wagtail application organized around small, purpose-specific applications and environment-specific settings.

Applications
------------

``basepage``
   Defines the custom Wagtail base page model used by all project page types, including shared SEO fields.

``home``
   Provides the site root home page.

``content``
   Provides the general-purpose content page.

``blocks``
   Contains reusable StreamField blocks.

``core``
   Contains site-wide functionality such as navigation, search, SEO helpers, canonical-host handling, storage utilities, and management commands.

Settings
--------

``{{ project_name }}.settings.base`` contains settings shared by all environments. ``{{ project_name }}.settings.dev`` contains local development settings. ``{{ project_name }}.settings.production`` contains production settings for Heroku, PostgreSQL, S3, CloudFront, and security.

``manage.py`` defaults to development settings locally. On Heroku, the presence of the ``DYNO`` environment variable causes management commands to default to production settings. An explicitly supplied ``DJANGO_SETTINGS_MODULE`` always takes precedence.

Storage
-------

Production static files and uploaded media are stored in a private Amazon S3 bucket. CloudFront provides public delivery while Origin Access Control (OAC) allows the S3 bucket itself to remain private.

Static files use the ``static/`` prefix, uploaded media use ``media/``, and database backups use ``backups/`` by default.
