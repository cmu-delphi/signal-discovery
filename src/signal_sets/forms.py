from django import forms

from signals.models import Pathogen, GeographicScope, Geography, SeverityPyramidRung
from signal_sets.models import SignalSet
from datasources.models import DataSource


class SignalSetFilterForm(forms.ModelForm):

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

    severity_pyramid_rungs = forms.ModelChoiceField(
        queryset=SeverityPyramidRung.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
    )

    data_source = forms.ModelChoiceField(
        queryset=DataSource.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
    )

    temporal_granularity = forms.ChoiceField(
        choices=[
            ("Daily", "Daily"),
            ("Weekly", "Weekly"),
            ("Hourly", "Hourly"),
        ],
        widget=forms.CheckboxSelectMultiple(),
    )

    class Meta:
        model = SignalSet
        fields: list[str] = [
            "pathogens",
            "geographic_scope",
            "available_geographies",
            "severity_pyramid_rungs",
            "data_source",
            "temporal_granularity"
        ]

    def __init__(self, *args, **kwargs) -> None:
        """
        Initialize the form.
        """
        super().__init__(*args, **kwargs)

        # Set required attribute to False and disable helptext for all fields
        for field_name, field in self.fields.items():
            field.required = False
            field.help_text = ""
            field.label = ""
