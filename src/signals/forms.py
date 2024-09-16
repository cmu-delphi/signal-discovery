from django import forms
from django.utils.translation import gettext_lazy as _

from signals.models import (
    Pathogen,
    Signal,
    GeographicScope,
    Geography,
    SeverityPyramidRung,
    SignalsDbView,
)


class SignalFilterForm(forms.ModelForm):

    id = forms.ModelMultipleChoiceField(
        queryset=Signal.objects.all(),
        required=False,
        widget=forms.MultipleHiddenInput,
    )
    active = forms.TypedMultipleChoiceField(
        choices=[(True, "Ongoing Surveillance Only")],
        coerce=bool,
        required=False,
        widget=forms.CheckboxSelectMultiple(),
    )

    pathogens = forms.ModelChoiceField(
        queryset=Pathogen.objects.all(), widget=forms.CheckboxSelectMultiple()
    )

    geographic_scope = forms.ModelChoiceField(
        queryset=GeographicScope.objects.all(), widget=forms.CheckboxSelectMultiple()
    )

    available_geographies = forms.ModelChoiceField(
        queryset=Geography.objects.all().order_by("display_order_number"),
        widget=forms.CheckboxSelectMultiple(),
    )

    severity_pyramid_rung = forms.ModelChoiceField(
        queryset=SeverityPyramidRung.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
    )

    class Meta:
        model = SignalsDbView

        fields: list[str] = [
            "id",
            "active",
            "pathogens",
            "geographic_scope",
            "available_geographies",
            "severity_pyramid_rung",
        ]

    def __init__(self, *args, **kwargs) -> None:
        """
        Initialize the form.
        """
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.required = False
            field.help_text = ""
            field.label = ""
