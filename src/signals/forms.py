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

from datasources.models import SourceSubdivision


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

    available_geography = forms.ModelChoiceField(
        queryset=Geography.objects.all().order_by("display_order_number"),
        widget=forms.CheckboxSelectMultiple(),
    )

    severity_pyramid_rung = forms.ModelChoiceField(
        queryset=SeverityPyramidRung.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
    )

    datasource = forms.MultipleChoiceField(
        choices=[], widget=forms.CheckboxSelectMultiple()
    )

    time_type = forms.ChoiceField(
        choices=[
            ("day", "Day"),
            ("week", "Week"),
        ],
        widget=forms.CheckboxSelectMultiple(),
    )

    from_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
        label=_("Available Since"),
    )

    to_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
        label=_("Available Until"),
    )

    signal_availability_days = forms.IntegerField(
        required=False, label=_("Available for at least (days)")
    )

    class Meta:
        model = SignalsDbView

        fields: list[str] = [
            "id",
            "active",
            "pathogens",
            "geographic_scope",
            "available_geography",
            "severity_pyramid_rung",
            "datasource",
            "time_type",
            "from_date",
            "to_date",
            "signal_availability_days",
        ]

    def __init__(self, *args, **kwargs) -> None:
        """
        Initialize the form.
        """
        super().__init__(*args, **kwargs)

        # Set required attribute to False and disable helptext for all fields
        # self.fields["available_geography"].queryset = self.fields["available_geography"].queryset.order_by("order_id")
        try:
            self.fields["datasource"].choices = set(
                SourceSubdivision.objects.values_list("display_name", "display_name")
            )
        except SourceSubdivision.DoesNotExist:
            self.fields["datasource"].choices = []
        for field_name, field in self.fields.items():
            field.required = False
            field.help_text = ""
            field.label = ""
        # self.fields['from_date'].label = _('Available Since')
        # self.fields['to_date'].label = _('Available Until')
        # self.fields['signal_availability_days'].label = _('Available for at least (days)')
