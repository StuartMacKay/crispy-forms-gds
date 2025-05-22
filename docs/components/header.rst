.. _Header: https://design-system.service.gov.uk/components/header/

######
Header
######
There is a `Header`_ component implemented in the ``gds/base.html`` template that
is include in the template pack. It is wrapped with a block tag, ``{% block hjeader %}``
so if you extend the base template you can override it if you need to.

The block implements the "Service name with navigation" variation of the different headers shown
on the Design System page. There are two main daughter blocks ``{% block header__logo %}``
for displaying the crown logo and "GOV.UK" and ``{% block header__service %}``

.. note::
    The header__logo block is specifically overridden in the Demo site as the
    author does not have permission to display the crown logo.

Within ``{% block header__service %}`` there are three further blocks: ``{% block header__service__url %}``
and ``{% block header__service__name %}`` where you can set the URL, and name for your site
and ``{% block header__service__navigation %}`` where you can set navigation links for
your site. This block is left empty for now.
