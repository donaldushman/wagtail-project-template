# Wagtail Project Template

An opinionated starter for Django/Wagtail projects.

The template is built around a custom `BasePage` from the beginning of the
project lifecycle. The configured Wagtail page model and its bootstrap
migrations are foundational architecture and should not be changed after
migrations have been applied without a planned database migration.

## Status

Initial development. The first milestone establishes the custom page model and
a minimal, testable Wagtail project before reusable site features are added.
