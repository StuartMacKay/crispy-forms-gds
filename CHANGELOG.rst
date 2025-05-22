Changelog
=========
All notable changes to this project will be documented in this file.
Only changes for the API functions are described here. Changes made
to the internals and developing the package are not included. Check
the git log for details.

The format is based on [Keep a Changelog](http://keepachangelog.com/).
This project adheres to [PEP440](https://www.python.org/dev/peps/pep-0440/)
and by implication, [Semantic Versioning](http://semver.org/).

Latest
------

2.0.1 (2025-01-11)
------------------
* Added setting for govuk frontend version to allow conditional HTML generation
* Changed Warning Text component to hide the "Warning" prefix to the message
* Fixed conditional radio buttons to reveal hidden fields when an option is selected
* Fixed project dependencies so django-crispy-forms 2.3 can be installed

2.0.0 (2024-12-30)
------------------
* Added support for Django 5.0, 5.1
* Dropped support for Django 4.2 LTS

1.0.0 (2024-12-30)
------------------
* Updated project to use uv
* Dropped support for Django 3.2 LTS
* Dropped support for django-crispy-forms 1.x
* Dropped support for python 3.8, minimum version is now 3.10
* Dropped the base template, use the `Page Template`_ instead
* Changed demo site to use `pre-compiled`_ govuk-frontend assets
* Changed the licence to the `MIT`_ license

.. _Page Template: https://design-system.service.gov.uk/styles/page-template/
.. _pre-compiled: https://frontend.design-system.service.gov.uk/install-using-precompiled-files/
.. _MIT: https://opensource.org/licenses/MIT

0.3.2 (2024-12-29)
------------------
* Added version compatibility matrix to README
* Moved virtualenv directory to .venv
* Removed Django 5.0 from test environments
* Removed tox-pyenv - it's not compatible with tox 4

0.3.1 (2024-02-14)
------------------
* Fix `Option overlap`_ in radios and checkboxes, where, if one option is
  a substring of another, then both are selected/checked.

.. _Option overlap: https://github.com/StuartMacKay/crispy-forms-gds/issues/82

0.3.0 (2024-02-12)
------------------
* Add `Conditional Radio buttons`_

.. _Conditional Radio buttons: https://design-system.service.gov.uk/components/radios/#conditionally-revealing-a-related-question

0.2.6 (2024-02-12)
------------------
* Updated to support django-crispy-forms 2.x
* Updated environments tested to add Django 5.0

0.2.5 (2024-02-09)
------------------
* Django 2.2 is no longer supported
* Updated environments tested to include Django 3.2 LTS, 4.0, 4.1, 4.2 LTS
* Updated environments tested to include all django-crispy-forms 1.x releases
* Updated packages used in demo

0.2.4 (2022-03-07)
------------------
* Password fields are styled correctly.

0.2.3 (2021-12-13)
------------------
* Django 4.0 support added.
* Confirmed support for python 3.9/3.10
* Fixed issues with DateInputField, thanks @ahernp & @NDevox.

0.2.2 (2021-01-07)
------------------
* Changed FormHelper now correctly translates Sizes into css classes.

0.2.1 (2020-05-25)
------------------
* Simplified webpack configuration for demo site.
* Synchronized demo site and package licences and versions.

0.2.0 (2020-05-16)
------------------
* Added hints to checkboxes and radios.
* Added contents summary to Accordion component sections.
* Added the fields and templates needed for the Date input component.
* Added template tags for back links, start buttons and breadcrumbs.
* Added a production-ready base template that can be used in sites.
* Added a Choice class to make setting hints and dividers on checkboxes and radio buttons cleaner and easier.
* Merged the templatetags so all you have to do is {% load crispy_forms_gds %}.
* Changed Table component to support a caption and CSS styling.
* Deleted the hints attribute on Field.checkboxes() and Field.radios()

0.1.0 (2020-04-28)
------------------
- Added all the form-level components from the Design System. The only one missing is Date input.

0.0.1 (2020-04-03)
------------------
- Added all the project files needed to generate the package documentation.
- Added all the project files needed to release the package to PyPI.
- Added a set of core templates for rendering forms.
- Added layout object for rendering submit buttons.
- Added tests for verifying text inputs are rendered correctly.
- Added Django site for showing how the forms are used.
