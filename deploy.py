import os

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "{{ project_name }}.settings.production",
)

import django
from django.core.management import call_command


django.setup()

call_command("migrate")
call_command("collectstatic", interactive=False)
