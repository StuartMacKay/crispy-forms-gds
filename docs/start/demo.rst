.. _crispy-forms-gds: https://github.com/StuartMacKay/crispy-forms-gds
.. _install nvm: https://github.com/nvm-sh/nvm
.. _makefile: https://github.com/StuartMacKay/crispy-forms-gds/blob/master/Makefile

=========
Demo Site
=========

If you checked out or downloaded the source for `crispy-forms-gds`_ from the
repository then you can run the Django demo site to see all Design System
components in action.

.. code-block:: console

    git clone git@github.com:StuartMacKay/crispy-forms-gds.git
    cd crispy-forms-gds

First, create a virtual environment:

.. code-block:: console

    uv venv

Activate it:

.. code-block:: console

    source .venv/bin/activate

Install all the dependencies:

.. code-block:: console

    uv sync

Next, copy and install the precompiled govuk-frontend files in the ``assets``
directory in the project root:

1. Download the pre-compiled files provided at bottom of each set of `GOV.UK Frontend
release notes`_.
2. Unzip the zip file.
3. Copy the files in ``assets/fonts`` to ``assets/fonts``.
4. Copy the files in ``assets/images`` to ``assets/images``.
5. Copy the file, assets/manifest.json to ``assets``.
6. Copy the .css and .css.map files to ``assets/stylesheets``.
7. Copy the .js and .js.map files to ``assets/javascripts``.
8. Edit ``demo/settings.py`` to set ``GDS_VERSION`` to the version you downloaded.

Create a copy of the .env.example file and edit it to set the version number of
the govuk-frontend you downloaded:

.. code-block:: console

    cp .env.example .env

Now, setup and run Django:

.. code-block:: console

    python manage.py migrate
    python manage.py runserver

Open http://localhost:8000/ in your browser to see forms built with `Django Crispy Forms`_
styled using the `GOV.UK Design System`_.

.. _GOV.UK Frontend release notes: https://github.com/alphagov/govuk-frontend/releases/latest
.. _Django Crispy Forms: https://github.com/maraujop/django-crispy-forms/
.. _GOV.UK Design System: https://design-system.service.gov.uk/
