.. _Radios: https://design-system.service.gov.uk/components/radios/

######
Radios
######
A `Radios`_ component is used when there is only one option allowed from a list. ::

    from django import forms

    from crispy_forms_gds.choices import Choice
    from crispy_forms_gds.helper import FormHelper
    from crispy_forms_gds.layout import Field, Layout, Size, Submit


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
            super(RadiosForm, self).__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.layout = Layout(
                Field.radios("name", legend_size=Size.MEDIUM, legend_tag="h1", inline=True),
                Field.radios(
                    "method",
                    legend_size=Size.MEDIUM,
                    small=True,
                ),
                Submit("submit", "Submit"),
            )

You can see this form live in the Demo site.

The set of radio buttons are wrapped in a <fieldset> with a <legend>. The field's
label used as the legend title. The keyword argument, ``legend_size`` is used to
change the size and weight of the font of the legend, otherwise the legend will
be the same size as body text, which is a bit unimposing. The ``Size`` class
defines a set of string constants, ``SMALL``, ``MEDIUM``, ``LARGE`` and ``EXTRA_LARGE``
to make things a little more readable but you can just use the corresponding values:
``'s'``, ``'m'``, ``'l'`` or ``'xl'`` directly if you prefer.

Im a multi-page form, where a single set of radio buttons is the only component on
a page, you can wrap the legend in an ``<h1>`` header tag by setting the ``legend_tag``
keyword argument to ``'h1'`` - leaving out the angle brackets. This avoids the duplication,
particularly for screen readers, of having a page title then the radio buttons' legend
effectively saying the same thing.

If you use the ``Choice`` class to create the list of choice for the field you
can set a ``hint`` for each item as needed. You can also set ``divider`` that will
display a separator <div> with a string after the radio button.

------------------
Conditional radios
------------------

A `Conditional radios`_ component is used when there are fields and/or content that
should be conditionally revealed once a particular answer has been selected. ::

    from django import forms

    from crispy_forms_gds.helper import FormHelper
    from crispy_forms_gds.layout import ConditionalQuestion, ConditionalRadios


    class ConditionalRadiosForm(forms.Form):
        how_would_you_like_to_be_contacted = forms.ChoiceField(
            choices=(
                ("phone", "By phone"),
                ("email", "By email"),
                ("no_contact", "Don't contact me"),
            ),
        )
        mobile_phone_number = forms.CharField()
        home_phone_number = forms.CharField()
        email_address = forms.EmailField()

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.layout = Layout(
                ConditionalRadios(
                    "how_would_you_like_to_be_contacted",
                    ConditionalQuestion(
                        "By phone",
                        "mobile_phone_number",
                        "home_phone_number",
                        HTML.p("Please enter either mobile or home")
                    ),
                    ConditionalQuestion(
                        "By email",
                        "email_address",
                    ),
                    "Don't contact me",
                ),
            )
