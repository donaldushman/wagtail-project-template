import os

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "{{ project_name }}.settings.production",
)

from django.core.management import call_command


call_command("migrate")
call_command("collectstatic", interactive=False)
