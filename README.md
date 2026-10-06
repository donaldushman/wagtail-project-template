# Wagtail Project Template

An opinionated starter for new Django/Wagtail projects.

The template provides a tested project structure and a common set of features used across Wagtail sites, while leaving project-specific content, branding, analytics, and integrations to the generated project.

Version 1.0.0 has been clean-room tested locally and on Heroku with PostgreSQL, private Amazon S3 storage, CloudFront delivery, protected Sphinx documentation, and database backups.

## What's Included

- Django 6.1 and Wagtail 8
- Custom Wagtail `BasePage` configured from the first migration
- Shared SEO fields and metadata helpers
- Generic `HomePage` and `ContentPage` page types
- Reusable StreamField blocks for headings, rich text, notes, links, images, cards, and card grids
- Bootstrap-based frontend structure
- Site navigation and search
- Site-wide Wagtail settings
- Wagtail draft sharing
- Broken-link auditing with `wagtail-linkaudit`
- Request filtering with `django-requestguard`
- Protected Sphinx technical documentation with `django-protected-docs`
- Private Amazon S3 storage with CloudFront delivery
- PostgreSQL database backups to S3 with retention cleanup
- Development and production settings
- Heroku deployment configuration
- Automated tests

Project-specific features such as branding, analytics and consent management, forms, third-party integrations, and application-specific page types are intentionally not included.

## Requirements

The generated project assumes:

- Python 3.14
- PostgreSQL
- Amazon S3 and CloudFront for production static files and media
- Heroku for the included production deployment configuration

Other hosting environments can be used by replacing or adapting the production settings and deployment configuration.

## Creating a Project

Use a descriptive kebab-case name for the repository or parent directory and a snake_case name for the Python project package.

For example:

- Repository: `pace-wi`
- Python package: `pace_wi`

Create the project directly in the repository root:

```console
mkdir my-project
cd my-project

python -m venv .venv
source .venv/bin/activate

pip install wagtail

wagtail start my_project . \
    --template=https://github.com/donaldushman/wagtail-project-template/archive/refs/tags/v1.0.0.zip

pip install -r requirements.txt
```

Using `.` as the destination keeps `manage.py`, the Django applications, documentation, and deployment files at the repository root rather than creating an additional nested directory.

The tagged template URL above uses the tested v1.0.0 release. Use the `main` branch only when intentionally testing current template development.

## Local Configuration

Copy the example environment file:

```console
cp .env.example .env
```

Update `.env` with the local PostgreSQL connection information.

Create an empty PostgreSQL database, then initialize the project:

```console
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Local management commands automatically use the development settings unless `DJANGO_SETTINGS_MODULE` is explicitly supplied.

## Important: Custom Base Page Model

The template configures:

```python
WAGTAIL_PAGE_MODEL = "basepage.BasePage"
```

from the beginning of the project's migration history.

This is foundational project architecture. Do not change the configured Wagtail page model after the database has been initialized without planning the required database and migration changes.

New page types should normally inherit from `BasePage`.

## Project Structure

The generated project contains the following primary applications:

- `basepage` — shared Wagtail base page model and SEO fields
- `home` — site root home page
- `content` — general-purpose content page
- `blocks` — reusable StreamField blocks
- `core` — navigation, search, SEO helpers, settings, storage, middleware, management commands, and Wagtail admin customizations

Environment-specific Django settings live under `<project_name>/settings/`.

Sphinx technical documentation lives under `docs/`.

## Technical Documentation

The generated project includes Sphinx documentation intended to become the application's technical guide.

Install the documentation dependencies and build the HTML:

```console
pip install -r docs/requirements.txt
cd docs
make html
```

The Wagtail Help menu includes a `<project name> Technical Guide` link. In deployed projects, `django-protected-docs` serves the built documentation at `/docs/` to staff users and redirects anonymous users through the Wagtail login.

The generated Sphinx documentation covers architecture, development, and deployment and should evolve with the individual project.

## Production Configuration

Production settings expect configuration for:

- `SECRET_KEY`
- `DATABASE_URL`
- `SITE_URL`
- `ALLOWED_HOSTS` when overriding the default
- `CSRF_TRUSTED_ORIGINS` when overriding the default
- AWS credentials
- S3 bucket and region
- CloudFront domain

See `app.json`, `.env.example`, and the generated Technical Guide for the current configuration details.

### S3 and CloudFront

The production architecture assumes a private S3 bucket with public access disabled. CloudFront provides public access to static files and uploaded media using Origin Access Control (OAC).

By default:

- static files use `static/`
- uploaded media use `media/`
- database backups use `backups/`

## Database Backups

The project includes:

```console
python manage.py backup_database
```

In production the command creates a PostgreSQL custom-format dump, uploads it to the private S3 bucket, and removes backups older than the configured retention period.

Backup scheduling is intentionally external to Django. Configure Heroku Scheduler or another scheduling service to run the command at the desired interval.

## Testing

Before deployment, run:

```console
python manage.py check
python manage.py test
```

When changing documentation, also verify that the Sphinx build succeeds:

```console
cd docs
make html
```

When upgrading Django, Wagtail, or reusable integrations, verify draft sharing, link auditing, request filtering, protected documentation, static/media storage, and database backups as appropriate.

## Deployment

The template includes `app.json`, a `Procfile`, and a release script for Heroku.

The release process runs database migrations and collects static files. On Heroku, `manage.py` detects the `DYNO` environment variable and automatically uses production settings.

Typical production verification includes:

```console
heroku run python manage.py check -a <app-name>
heroku run python manage.py backup_database -a <app-name>
```

See the generated Technical Guide for AWS/CloudFront architecture, environment configuration, backup behavior, and production cutover guidance.

## After Generation

A generated project is an independent application. Customize its page types, blocks, templates, styles, settings, documentation, integrations, and deployment configuration for the project it serves.

The template is intended to provide a reliable starting point, not to keep generated projects synchronized with future template releases.
