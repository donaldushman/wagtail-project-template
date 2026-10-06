Development
===========

Project Naming
--------------

Use a descriptive kebab-case name for the repository or parent directory and a snake_case name for the generated Python package. For example, use ``pace-wi`` for the repository and ``pace_wi`` for the Python package. Prefer a descriptive package name over a generic name such as ``config``.

Create a Project
----------------

Create and activate a virtual environment, then install Wagtail before generating the project:

.. code-block:: console

   $ mkdir my-project
   $ cd my-project
   $ python -m venv .venv
   $ source .venv/bin/activate
   $ pip install wagtail
   $ wagtail start my_project . --template=<template-url>
   $ pip install -r requirements.txt

Copy ``.env.example`` to ``.env`` and configure the local PostgreSQL connection.

Database Setup
--------------

Create an empty PostgreSQL database, then run:

.. code-block:: console

   $ python manage.py migrate

The project uses a custom Wagtail page model from the first migration. Do not change ``WAGTAIL_PAGE_MODEL`` after the database has been initialized without planning the corresponding migration work.

Development Server
------------------

.. code-block:: console

   $ python manage.py runserver

Useful Checks
-------------

.. code-block:: console

   $ python manage.py check
   $ python manage.py test

The starter includes Wagtail draft sharing, link auditing, and request filtering. Confirm these integrations remain functional when upgrading Django or Wagtail.
