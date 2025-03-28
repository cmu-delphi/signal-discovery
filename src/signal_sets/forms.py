from django import forms

from signals.models import Pathogen, GeographicScope, Geography, SeverityPyramidRung
from signal_sets.models import SignalSet
from datasources.models import DataSource


class SignalSetFilterForm(forms.ModelForm):

    pathogens = forms.ModelChoiceField(
        queryset=Pathogen.objects.filter(
            # id__in=SignalSet.objects.values_list("pathogens", flat="True")
            used_in="signal_sets"
        ),
        widget=forms.CheckboxSelectMultiple(),
    )

    geographic_scope = forms.ModelChoiceField(
        queryset=GeographicScope.objects.filter(
            # id__in=SignalSet.objects.values_list("geographic_scope", flat="True")
            used_in="signal_sets"
        ),
        widget=forms.CheckboxSelectMultiple(),
    )

    available_geographies = forms.ModelChoiceField(
        queryset=Geography.objects.filter(
            # id__in=SignalSet.objects.values_list("available_geographies", flat="True")
            used_in="signal_sets"
        ).order_by("display_order_number"),
        widget=forms.CheckboxSelectMultiple(),
    )

    severity_pyramid_rungs = forms.ModelChoiceField(
        queryset=SeverityPyramidRung.objects.filter(
            # id__in=SignalSet.objects.values_list("severity_pyramid_rungs", flat="True")
            used_in="signal_sets"
        ).order_by("display_order_number"),
        widget=forms.CheckboxSelectMultiple(),
    )

    data_source = forms.ModelChoiceField(
        queryset=DataSource.objects.filter(
            id__in=SignalSet.objects.values_list("data_source", flat="True")
        ),
        widget=forms.CheckboxSelectMultiple(),
    )

    temporal_granularity = forms.ChoiceField(
        choices=[
            ("Annually", "Annually"),
            ("Monthly", "Monthly"),
            ("Weekly", "Weekly"),
            ("Daily", "Daily"),
            ("Hourly", "Hourly"),
            ("Other", "Other")
        ],
        widget=forms.CheckboxSelectMultiple(),
    )

    temporal_scope_end = forms.ChoiceField(
        choices=[
            ("Ongoing", "Ongoing Surveillance Only"),
        ],
        required=False,
        widget=forms.CheckboxSelectMultiple(),
    )

    location_search = forms.CharField(
        label=("Location Search"),
        widget=forms.TextInput(),
    )

    class Meta:
        model = SignalSet
        fields: list[str] = [
            "pathogens",
            "geographic_scope",
            "available_geographies",
            "severity_pyramid_rungs",
            "data_source",
            "temporal_granularity",
            "temporal_scope_end"
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
