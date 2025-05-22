================
Crispy Forms GDS
================

A `GOV.UK Design System`_ template pack for `Django Crispy Forms`_, for simple and
powerful form generation which is compliant with GDS usability and accessibility
guidelines.

.. _Django Crispy Forms: https://github.com/maraujop/django-crispy-forms/
.. _GOV.UK Design System: https://design-system.service.gov.uk/

.. image:: https://codecov.io/gh/StuartMacKay/crispy-forms-gds/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/StuartMacKay/crispy-forms-gds

.. image:: https://badge.fury.io/py/crispy-forms-gds.svg
    :target: https://pypi.python.org/pypi/crispy-forms-gds/

.. image:: https://img.shields.io/pypi/pyversions/crispy-forms-gds.svg
    :target: https://pypi.python.org/pypi/crispy-forms-gds/


Compatibility
=============
+-------------------+--------------------------+---------------------+------------------+
| crispy-forms-gds  | Government Design System | django-crispy-forms | django           |
+-------------------+--------------------------+---------------------+------------------+
| 1.x (maintenance) | 5.0 - 5.2                | 2.0 - 2.3           | 4.2 LTS          |
+-------------------+--------------------------+---------------------+------------------+
| 2.x (current)     | 5.0 - 5.8                | 2.0 - 2.3           | 5.0, 5.1         |
+-------------------+--------------------------+---------------------+------------------+

Crispy-forms-gds has a rich set of components for building pages, but not everything
from the Government Design System is implemented. Version 1.x will still be updated to
add the missing components while Django 4.2 LTS is still supported - until April 2026.
Only reported bugs will be fixed after this date. Version 2.x is the current release,
and releases will be made as the set of components supported expands.

The Government Design System versions will be updated as each release is tested.

For information the components which have not yet been implemented. Check the
`issues`_ for the current status. If you have a pressing need for a particular
component, then, please, open an issue.

.. _issues: https://github.com/StuartMacKay/crispy-forms-gds/issues

Quickstart
==========

This is a minimal howto without options or details - see the
`crispy-forms-gds documentation <http://crispy-forms-gds.readthedocs.io/>`_ for full
instructions for installation and usage.

Install using pip::

    pip install crispy-forms-gds

Add to installed apps, with settings to tell django-crispy-forms to use this theme,
along with the version number of the govuk frontend you are using::

    INSTALLED_APPS = [
      ...
      'crispy_forms',
      'crispy_forms_gds',
    ]
    CRISPY_ALLOWED_TEMPLATE_PACKS = ["gds"]
    CRISPY_TEMPLATE_PACK = "gds"
    CRISPY_GDS_FRONTEND_VERSION = "5.0.0"

Build a regular crispy form using layout objects from ``crispy_forms_gds``::

    from django import forms

    from crispy_forms_gds.helper import FormHelper
    from crispy_forms_gds.layout import Submit


    class SimpleForm(forms.Form):

        name = forms.CharField(
            label="Name",
            help_text="Your full name.",
            widget=forms.TextInput(),
            error_messages={
                "required": "Enter your name as it appears on your passport"
            }
        )

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.add_input(Submit("submit", "Submit"))


Render the form in your templates as normal::

    {% load crispy_forms_tags %}
    {% crispy form %}


Examples
========

The template pack supports all the basic components listed in the `GOV.UK Design
System`_. Here are some examples taken from the demo site included in the project.

Accordion
---------

.. _Accordion: https://design-system.service.gov.uk/components/accordion/

Layout components, such as the `Accordion`_ let you generate complex forms with
multiple sections::

    from django import forms

    from crispy_forms_gds.helper import FormHelper
    from crispy_forms_gds.layout import HTML, Accordion, AccordionSection, Layout


    class AccordionForm(forms.Form):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.layout = Layout(
                Accordion(
                    AccordionSection(
                        "Writing well for the web",
                        HTML.p("This is the content for Writing well for the web."),
                        summary="An introduction to clear and concise writing.",
                    ),
                    AccordionSection(
                        "Writing well for specialists",
                        HTML.p("This is the content for Writing well for specialists."),
                    ),
                    AccordionSection(
                        "Know your audience",
                        HTML.p("This is the content for Know your audience."),
                    ),
                    AccordionSection(
                        "How people read",
                        HTML.p("This is the content for How people read."),
                    ),
                )
            )

.. image:: docs/screenshots/accordion.png

Radio Buttons
-------------

.. _Radio: https://design-system.service.gov.uk/components/radios/
.. _Select: https://design-system.service.gov.uk/components/select/

ChoiceFields can be displayed as `Select`_ or `Radio`_ components. Radio buttons also support
Design System features such as sizing, hinting and dividers::

    from django import forms

    from crispy_forms_gds.choices import Choice
    from crispy_forms_gds.helper import FormHelper
    from crispy_forms_gds.layout import Button, Field, Layout, Size


    class RadiosForm(forms.Form):

        name = forms.ChoiceField(
            choices=(("yes", "Yes"), ("no", "No")),
            widget=forms.RadioSelect,
            label="Have you changed your name?",
            help_text="This includes changing your last name or spelling your name differently.",
            error_messages={"required": "Enter whether your name has changed"},
        )

        METHODS = (
            Choice("email", "Email", hint="Do not use an email address from work"),
            Choice("phone", "Phone", divider="Or"),
            Choice("text", "Text message"),
        )

        method = forms.ChoiceField(
            choices=METHODS,
            widget=forms.RadioSelect,
            label="How would you like to be contacted?",
            help_text="Select the options that is best for you.",
            error_messages={
                "required": "Select the best way to send a confirmation message"
            },
        )

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.layout = Layout(
                Field.radios("name", legend_size=Size.MEDIUM, legend_tag="h1", inline=True),
                Field.radios("method", legend_size=Size.MEDIUM, small=True),
                Button("submit", "Submit"),
            )

.. image:: docs/screenshots/radio-buttons.png

Validation Errors
-----------------

.. _Error Summary: https://design-system.service.gov.uk/components/error-summary/
.. _Error Message: https://design-system.service.gov.uk/components/error-message/

Forms fully support the `Error Message`_ and `Error Summary`_ components with no
extra effort on your part::

    from django import forms

    from crispy_forms_gds.helper import FormHelper
    from crispy_forms_gds.layout import (
        Button,
        Field,
        Fieldset,
        Fixed,
        Fluid,
        Layout,
        Size,
    )


    class UserForm(forms.Form):

        name = forms.CharField(
            label="Your name",
            help_text="Enter your name as it appears on your passport.",
        )

        email = forms.CharField(
            label="Email",
            help_text="Enter your email address.",
            widget=forms.EmailInput,
        )

        phone = forms.CharField(
            label="Phone",
            help_text="Enter your home or mobile telephone number.",
        )

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.label_size = Size.SMALL
            self.helper.layout = Layout(
                Fieldset(
                    Field.text("name"),
                    Field.text("email", field_width=Fluid.TWO_THIRDS),
                    Field.text("phone", field_width=Fixed.TEN),
                ),
                Button("submit", "Submit"),
            )

.. image:: docs/screenshots/validation-errors.png

Demo
====
If you checkout the code from the repository, there is a Django site you can run to see
the forms in action:

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

1. Download the pre-compiled files provided at bottom of each `GOV.UK Frontend
release note`_.
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

.. _GOV.UK Frontend release note: https://github.com/alphagov/govuk-frontend/releases/latest

Project Information
===================

Crispy Forms GDS is a community supported tool of the GOV.UK Design System. The
Design System team is not responsible for it and cannot support you with using it.
Contact Stuart MacKay directly if you need help or you want to request a feature.
The easiest way to do this is to open an issue at our GitHub repository.

* Documentation: https://crispy-forms-gds.readthedocs.io/en/latest/
* Issues: https://github.com/StuartMacKay/crispy-forms-gds/issues
* Repository: https://github.com/StuartMacKay/crispy-forms-gds/

The app is tested with Python 3.10+, and version 1.x officially supports Django
4.2 LTS, and `Django Crispy Forms`_ 2.x. Version 2.x supports Django 5.0, 5.1,
and Django Crispy Forms 2.x. The app simply generates HTML, so it can probably
be used with earlier versions of Django and Django Crispy Forms.

Crispy Forms GDS is released under the terms of the `MIT`_ license.

.. _MIT: https://opensource.org/licenses/MIT
