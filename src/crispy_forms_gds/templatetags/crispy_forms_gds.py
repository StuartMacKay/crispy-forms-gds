from django import forms, template
from django.conf import settings
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from crispy_forms.utils import TEMPLATE_PACK

register = template.Library()


@register.inclusion_tag("gds/layout/breadcrumbs.html")
def breadcrumbs(crumbs):
    """
    Inclusion tag that renders the HTML needed to display Breadcrumbs component.

    Examples::

        {% load crispy_forms_gds %}
        ...
        {% breadcrumbs crumbs %}

    Args:
        crumbs: a list of 2-tuples. The tuple is made up of the link title followed
            by the link URL.

    """
    return {"crumbs": crumbs}


@register.simple_tag
def back_link(url, title=None):
    """
    Template tag that returns the HTML needed to display a URL as a Back link component.

    Examples::

        {% load crispy_forms_gds %}
        ...
        {% url "home" as home_url %}
        {% back_link home_url %}

    Args:
        url (str): the URL for the link.
        title (str, optional): the title if the default "Back" is not suitable.

    """
    if title is None:
        title = _("Back")
    return format_html('<a href="{}" class="govuk-back-link">{}</a>', url, title)


@register.simple_tag
def button_link(url, title):
    """
    Template tag that returns the HTML needed to display a link as a Button component.

    Examples::

        {% load crispy_forms_gds %}
        ...
        {% button_link url title %}

    Args:
        url (str): the URL for the link.
        title (str): the title of the button.

    """
    return format_html(
        '<a href="{}" role="button" draggable="false" class="govuk-button" data-module="govuk-button">{}</a>',  # noqa
        url,
        title,
    )


@register.simple_tag
def button_start(url, title):
    """
    Template tag that returns the HTML needed to display a Start button.

    Examples::

        {% load crispy_forms_gds %}
        ...
        {% button_start url title %}

    Args:
        url (str): the URL for the link.
        title (str): the title of the button.

    """
    html = """
    <a href="{}" role="button" draggable="false"
       class="govuk-button govuk-button--start" data-module="govuk-button">
        {}
      <svg class="govuk-button__start-icon" xmlns="http://www.w3.org/2000/svg"
           width="17.5" height="19" viewBox="0 0 33 40" aria-hidden="true" focusable="false">
        <path fill="currentColor" d="M0 0h13l20 20-20 20H0l20-20z" />
      </svg>
    </a>"""  # noqa
    return format_html(html, url, title)


@register.inclusion_tag("gds/layout/error_summary.html")
def error_summary(form):
    """
    Template tag that renders the list of errors from a form.
    """
    return {"form": form}


@register.filter
def dict_lookup(d, value):
    """
    Template filter that looks up a value from a dict.
    """
    return d.get(value)


@register.filter
def dict_pop(d, key):
    """
    Template filter that looks removes a key-value pair from a dict.
    """
    return d.pop(key)


@register.filter
def field_errors(bound_field):
    """
    Template tag that returns the set of errors indexed by field id.

    Each key-value pair in the dict is the id of the field and the
    list of errors for that field. The items are returned rather than
    the dict to get over a limitation in the template syntax.

    """
    seen = []
    errors = {}
    if hasattr(bound_field.field, "fields"):
        for idx, subfield in enumerate(bound_field.field.fields):
            key = "%s_%d" % (bound_field.auto_id, idx)
            subfield_errors = getattr(subfield.widget, "errors", [])
            errors[key] = subfield_errors
            seen.extend(subfield_errors)
    for error in bound_field.errors:
        if error not in seen:
            errors.setdefault(bound_field.auto_id, [])
            errors[bound_field.auto_id].append(error)
    return errors.items()


@register.filter
def is_checkbox(field):
    """
    Template filter that returns True if the field is a checkbox, False otherwise.
    """
    return isinstance(field.field.widget, forms.CheckboxInput)


@register.filter
def is_radios(field):
    """
    Template filter that returns True if the field is a set of radio
    buttons field, False otherwise.
    """
    if isinstance(field.field.widget, forms.RadioSelect):
        return field.field.widget.input_type == "radio"
    return False


@register.filter
def is_select(field):
    """
    Template filter that returns True if the field is a drop-down select
    field, False otherwise.
    """
    return isinstance(field.field.widget, forms.Select)


@register.filter
def is_checkboxes(field):
    """
    Template filter that returns True if the field is set of checkboxes,
    False otherwise.
    """
    if isinstance(field.field.widget, forms.CheckboxSelectMultiple):
        return field.field.widget.input_type == "checkbox"
    return False


@register.filter
def is_file(field):
    """
    Template filter that returns True if the field is a file upload button,
    False otherwise.
    """
    return isinstance(field.field.widget, forms.FileInput)


@register.filter
def is_multivalue(field):
    """
    Template filter that returns True if the field is a multi-value field,
    False otherwise.
    """
    return isinstance(field.field.widget, forms.MultiWidget)


def pairwise(iterable):
    """
    Splits a list of items into pairs: s -> (s0,s1), (s2,s3), (s4, s5), ...
    """
    a = iter(iterable)
    return zip(a, a)


class CrispyGDSFieldNode(template.Node):
    """
    The TemplateNode used for rendering a field from the template pack.

    """

    def __init__(self, field, attrs):
        self.field = field
        self.attrs = attrs
        self.html5_required = "html5_required"

    def render(self, context):  # noqa: C901
        # Nodes are not threadsafe so we must store and look up our instance
        # variables in the current rendering context first
        if self not in context.render_context:
            context.render_context[self] = (
                template.Variable(self.field),
                self.attrs,
                template.Variable(self.html5_required),
            )

        field, attrs, html5_required = context.render_context[self]
        field = field.resolve(context)
        try:
            html5_required = html5_required.resolve(context)
        except template.VariableDoesNotExist:
            html5_required = False

        # Pick up the template pack if it has been overridden in FormHelper
        template_pack = context.get("template_pack", TEMPLATE_PACK)

        # There are special django widgets that wrap actual widgets,
        # such as forms.widgets.MultiWidget, admin.widgets.RelatedFieldWidgetWrapper
        widgets = getattr(
            field.field.widget,
            "widgets",
            [getattr(field.field.widget, "widget", field.field.widget)],
        )

        if template_pack == "gds":
            if is_multivalue(field):
                error_widgets = [field.widget for field in field.field.fields]
                error_count = sum(
                    len(getattr(widget, "errors", [])) for widget in error_widgets
                )
            else:
                error_widgets = None
                error_count = 0

        if isinstance(attrs, dict):
            attrs = [attrs] * len(widgets)

        converters = {
            "checkboxinput": "govuk-checkboxes__input",
            "select": "govuk-select",
            "textinput": "govuk-input",
            "emailinput": "govuk-input",
            "passwordinput": "govuk-input",
            "textarea": "govuk-textarea",
            "clearablefileinput": "govuk-file-upload",
        }
        converters.update(getattr(settings, "CRISPY_CLASS_CONVERTERS", {}))

        for widget_idx, (widget, attr) in enumerate(zip(widgets, attrs)):
            class_name = widget.__class__.__name__.lower()
            class_name = converters.get(class_name, class_name)

            if class_name:
                css_class = class_name.split()
            else:
                css_class = []

            for attr_css_class in widget.attrs.get("class", "").split():
                if attr_css_class not in css_class:
                    css_class.append(attr_css_class)

            css_class = " ".join(css_class)

            if (
                template_pack == "bootstrap3"
                and not is_checkbox(field)
                and not is_file(field)
                and not is_multivalue(field)
            ):
                css_class += " form-control"
                if field.errors:
                    css_class += " form-control-danger"

            if template_pack == "bootstrap4" and not is_multivalue(field):
                if not is_checkbox(field):
                    css_class += " form-control"
                    if is_file(field):
                        css_class += "-file"
                if field.errors:
                    css_class += " is-invalid"

            if template_pack == "gds":

                # The ability to override input_type was added to avoid having to
                # create new widgets. However, as a result, the browser validates
                # the field and displays a red border with no feedback to the user.
                # That is at odds with with the way the Design System reports errors.
                # However this is being left in for now until the "conflict" is better
                # understood - it might be useful to somebody at some point.

                if hasattr(widget, "input_type") and "input_type" in widget.attrs:
                    widget.input_type = widget.attrs.pop("input_type")

                if field.help_text and not is_multivalue(field):
                    widget.attrs["aria-describedby"] = "%s_hint" % field.auto_id

                if (
                    "class" in widget.attrs
                    and "govuk-js-character-count" in widget.attrs["class"]
                ):

                    # The javascript that updates the span containing character count
                    # as the user types expects the id to end in '-info'. Anything else
                    # won't work.

                    if widget.attrs["aria-describedby"]:
                        widget.attrs["aria-describedby"] += " %s-info" % field.auto_id
                    else:
                        widget.attrs["aria-describedby"] = "%s-info" % field.auto_id

                if field.errors:

                    widget_class_name = widget.__class__.__name__

                    if widget_class_name in ["EmailInput", "Select", "TextInput", "Textarea"]:
                        if is_multivalue(field):
                            if error_count == 0:
                                css_class += " govuk-input--error"
                            elif getattr(error_widgets[widget_idx], "errors", None):
                                css_class += " govuk-input--error"
                        else:
                            css_class += " govuk-input--error"
                    elif widget_class_name in ["FileInput", "ClearableFileInput"]:
                        css_class += " govuk-file-upload--error"

                    if not field.help_text:
                        widget.attrs["aria-describedby"] = ""

                    for error_idx, error in enumerate(field.errors, start=1):
                        css_error_class = "%s_%d_error" % (field.auto_id, error_idx)

                        if is_multivalue(field):
                            if getattr(error_widgets[widget_idx], "errors", None):
                                if error in error_widgets[widget_idx].errors:
                                    if "aria-describedby" not in widget.attrs:
                                        widget.attrs["aria-describedby"] = ""

                                    if widget.attrs["aria-describedby"]:
                                        widget.attrs["aria-describedby"] += " "

                                    widget.attrs["aria-describedby"] += css_error_class
                        else:
                            if "aria-describedby" not in widget.attrs:
                                widget.attrs["aria-describedby"] = ""

                            if widget.attrs["aria-describedby"]:
                                widget.attrs["aria-describedby"] += " "

                            widget.attrs["aria-describedby"] += css_error_class

            widget.attrs["class"] = css_class

            # HTML5 required attribute
            if (
                html5_required
                and field.field.required
                and "required" not in widget.attrs
            ):
                if field.field.widget.__class__.__name__ != "RadioSelect":
                    widget.attrs["required"] = "required"

            for attribute_name, attribute in attr.items():
                attribute_name = template.Variable(attribute_name).resolve(context)

                if attribute_name in widget.attrs:
                    widget.attrs[attribute_name] += " " + template.Variable(
                        attribute
                    ).resolve(context)
                else:
                    widget.attrs[attribute_name] = template.Variable(attribute).resolve(
                        context
                    )

        return str(field)


@register.tag(name="crispy_gds_field")
def crispy_gds_field(parser, token):
    """
    The template tag used to render fields from the template pack.

    Examples: ::

        {% crispy_gds_field field attrs %}

    The code was copied over verbatim from ``django-crispy-forms``. Any additions
    are clearly marked with a check to see if the 'gds' template pack is being
    used.

    This template tag is only used within the gds/field.html template and you
    almost certainly will not have to deal with it, even if you are laying out a
    form explicitly.

    """
    token = token.split_contents()
    field = token.pop(1)
    attrs = {}

    # We need to pop tag name, or pairwise would fail
    token.pop(0)
    for attribute_name, value in pairwise(token):
        attrs[attribute_name] = value

    return CrispyGDSFieldNode(field, attrs)
