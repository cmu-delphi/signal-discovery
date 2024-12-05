from django import forms
from django.utils.translation import gettext_lazy as _

from signals.models import (
    Signal,
    Pathogen,
    GeographicScope,
    Geography,
    SeverityPyramidRung,
    SignalsDbView,
)

from datasources.models import SourceSubdivision


class SignalFilterForm(forms.ModelForm):

    active = forms.TypedMultipleChoiceField(
        choices=[(True, "Ongoing Surveillance Only")],
        coerce=bool,
        widget=forms.CheckboxSelectMultiple(),
    )

    pathogens = forms.ModelChoiceField(
        queryset=Pathogen.objects.filter(id__in=Signal.objects.values_list("pathogen", flat=True)), widget=forms.CheckboxSelectMultiple()
    )

    geographic_scope = forms.ModelChoiceField(
        queryset=GeographicScope.objects.filter(id__in=Signal.objects.values_list("geographic_scope", flat=True)), widget=forms.CheckboxSelectMultiple()
    )

    available_geography = forms.ModelChoiceField(
        queryset=Geography.objects.filter(id__in=Signal.objects.values_list("available_geography", flat=True)).order_by("display_order_number"),
        widget=forms.CheckboxSelectMultiple(),
    )

    severity_pyramid_rung = forms.ModelChoiceField(
        queryset=SeverityPyramidRung.objects.filter(id__in=Signal.objects.values_list("severity_pyramid_rung", flat=True)),
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
        widget=forms.DateInput(attrs={"type": "date"}),
        label=_("Available Since"),
    )

    to_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}),
        label=_("Available Until"),
    )

    signal_availability_days = forms.IntegerField(
        label=_("Available for at least (days)")
    )

    class Meta:
        model = SignalsDbView

        fields: list[str] = [
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

        try:
            self.fields["datasource"].choices = set(
                SourceSubdivision.objects.filter(id__in=Signal.objects.values_list("source", flat=True)).values_list("display_name", "display_name")
            )
        except SourceSubdivision.DoesNotExist:
            self.fields["datasource"].choices = []

        # Set required attribute to False and disable helptext for all fields
        for field_name, field in self.fields.items():
            field.required = False
            field.help_text = ""
            field.label = ""
        self.fields["from_date"].label = _("Available Since")
        self.fields["to_date"].label = _("Available Until")
        self.fields["signal_availability_days"].label = _(
            "Available for at least (days)"
        )
