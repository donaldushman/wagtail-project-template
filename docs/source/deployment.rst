Deployment
==========

Heroku
------

The project includes ``app.json`` and a ``Procfile`` for Heroku deployment. The release process runs migrations and collects static files before the web dyno starts.

On Heroku, ``manage.py`` detects the ``DYNO`` environment variable and uses production settings by default. One-off commands therefore work normally:

.. code-block:: console

   $ heroku run python manage.py check -a <app-name>
   $ heroku run python manage.py createsuperuser -a <app-name>

Environment Variables
---------------------

Production requires the application secret, database connection, canonical site URL, and AWS/CloudFront configuration. See ``app.json`` and ``.env.example`` for the current variables.

``SITE_URL`` is the canonical public URL for the application and is separate from Django ``ALLOWED_HOSTS``. Production accepts ``.herokuapp.com`` by default so a newly provisioned app can run before its final domain is available. Set ``ALLOWED_HOSTS`` at cutover when tighter host validation is desired.

``CSRF_TRUSTED_ORIGINS`` defaults to ``SITE_URL`` and can also be overridden through the environment.

S3 and CloudFront
-----------------

The production architecture assumes a private S3 bucket with public access disabled, CloudFront as the public endpoint for static files and media, CloudFront Origin Access Control (OAC) for access to S3, and AWS credentials available to Django for uploads and static collection. The S3 bucket should not be made public to serve application assets.

Database Backups
----------------

The project includes a PostgreSQL backup command:

.. code-block:: console

   $ python manage.py backup_database

In production this runs ``pg_dump``, uploads the dump to the private S3 bucket, and removes backups older than the configured retention period. Defaults are ``DATABASE_BACKUP_LOCATION=backups`` and ``DATABASE_BACKUP_RETENTION=30``. Retention is measured in days and must be at least 1.

Scheduling is intentionally not part of the Django project. Configure Heroku Scheduler or another scheduling service to run the command nightly.

Production Cutover
------------------

A typical cutover includes configuring the final domain and DNS, enabling and verifying TLS, updating ``SITE_URL``, setting the desired ``ALLOWED_HOSTS`` and CSRF origins, and confirming the Wagtail Site hostname. Enable additional security settings such as HSTS only after the production domain and HTTPS configuration have been verified.
