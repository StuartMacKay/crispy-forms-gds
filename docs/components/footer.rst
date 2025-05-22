.. _Footer: https://design-system.service.gov.uk/components/footer/

######
Footer
######
There is a `Footer`_ component implemented in the ``gds/base.html`` template that
is include in the template pack. It is wrapped with a block tag ``{% block footer %}``
so if you extend the base template you can override it if you need to.

Currently the footer only contains the meta information from the Design System site,
which includes the licence terms and the crown copyright symbol. This is wrapped
in a ``{% block footer__meta %}`` tag.

.. note::
    The footer__meta block is specifically overridden in the Demo site as the
    author does not have permission to display the crown copyright symbol.

There is also an empty block for site navigation, ``{% block footer__navigation %}``, but
it is really only intended as a guide - the footer section has quite a bit of variation
since the content is tied completely to the implementation of each site.
