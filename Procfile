release: python manage.py migrate --settings={{ project_name }}.settings.production && python manage.py collectstatic --noinput --settings={{ project_name }}.settings.production
web: gunicorn {{ project_name }}.wsgi
