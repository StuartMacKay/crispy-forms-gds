"""
Tests to verify radio buttons are rendered correctly.

"""

import os

from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import Field, Layout, Size
from tests.unit.forms import RadiosChoiceForm, RadiosForm, RadiosInitialForm
from tests.unit.utils import TEST_DIR, parse_contents, parse_form

RESULT_DIR = os.path.join(TEST_DIR, "layout", "results", "radios")


def test_initial_attributes():
    """Verify all the gds attributes are displayed."""
    form = RadiosForm(initial={"method": "email"})
    form.helper = FormHelper()
    form.helper.layout = Layout(Field.radios("method"))
    assert parse_form(form) == parse_contents(RESULT_DIR, "initial.html")


def test_overlapping_options():
    """Verify that if an selected string option is a substring of another it is not checked.

    Added to confirm, https://github.com/StuartMacKay/crispy-forms-gds/issues/82
    where an option is selected if the initial value matches any part of the
    option value, i.e. an initial value of 'phone' matches an option with the
    value 'mobile_phone', so both boxes are checked.
    """
    form = RadiosInitialForm(initial={"method": "mobile_phone"})
    form.helper = FormHelper()
    form.helper.layout = Layout(Field.radios("method"))
    assert parse_form(form) == parse_contents(RESULT_DIR, "initial_overlapping.html")


def test_validation_error_attributes():
    """Verify all the gds error attributes are displayed."""
    form = RadiosForm(data={"method": ""})
    assert not form.is_valid()
    assert parse_form(form) == parse_contents(RESULT_DIR, "validation_errors.html")


def test_choices():
    """Verify hints and dividers are displayed."""
    form = RadiosChoiceForm(initial={"method": "email"})
    form.helper = FormHelper()
    form.helper.layout = Layout(Field.radios("method"))
    assert parse_form(form) == parse_contents(RESULT_DIR, "choices.html")


def test_small():
    """Verify size of the radio buttons can be changed."""
    form = RadiosForm()
    form.helper = FormHelper()
    form.helper.layout = Layout(Field("method", context={"radios_small": True}))
    assert parse_form(form) == parse_contents(RESULT_DIR, "buttons_small.html")


def test_inline():
    """Verify radio buttons can be displayed in a row."""
    form = RadiosForm()
    form.helper = FormHelper()
    form.helper.layout = Layout(Field("method", context={"radios_inline": True}))
    assert parse_form(form) == parse_contents(RESULT_DIR, "buttons_inline.html")


def test_show_legend_as_heading():
    """Verify the field legend can be displayed as the page heading."""
    form = RadiosForm()
    form.helper = FormHelper()
    form.helper.layout = Layout(Field("method", context={"legend_tag": "h1"}))
    assert parse_form(form) == parse_contents(RESULT_DIR, "legend_heading.html")


def test_change_legend_size():
    """Verify size of the field legend can be changed from the default."""
    form = RadiosForm()
    form.helper = FormHelper()
    form.helper.layout = Layout(
        Field("method", context={"legend_size": Size.for_legend("l")})
    )
    assert parse_form(form) == parse_contents(RESULT_DIR, "legend_size.html")


def test_no_legend():
    """Verify field is rendered correctly if no label is given."""
    form = RadiosForm()
    form.fields["method"].label = ""
    assert parse_form(form) == parse_contents(RESULT_DIR, "no_legend.html")


def test_no_help_text():
    """Verify field is rendered correctly if no help text is given."""
    form = RadiosForm()
    form.fields["method"].help_text = ""
    assert parse_form(form) == parse_contents(RESULT_DIR, "no_help_text.html")


def test_no_help_text_errors():
    """Verify all the gds error attributes are displayed if no help text is given."""
    form = RadiosForm(data={"method": ""})
    form.fields["method"].help_text = ""
    assert parse_form(form) == parse_contents(RESULT_DIR, "no_help_text_errors.html")
