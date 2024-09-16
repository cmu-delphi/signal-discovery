from django import forms
from django.utils.translation import gettext_lazy as _

from datasources.models import SourceSubdivision
from signals.models import (
    Signal,
    Pathogen,
    GeographicScope,
    SeverityPyramidRung,
)


class SignalFilterForm(forms.ModelForm):

    id = forms.ModelMultipleChoiceField(
        queryset=Signal.objects.all(),
        required=False,
        widget=forms.MultipleHiddenInput,
    )
    pathogen = forms.ModelMultipleChoiceField(
        queryset=Pathogen.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple(),
    )
    active = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(),
    )
    source = forms.MultipleChoiceField(
        choices=[],
        required=False,
        widget=forms.CheckboxSelectMultiple(),
    )
    time_type = forms.MultipleChoiceField(
        choices=[],
        required=False,
        widget=forms.CheckboxSelectMultiple(),
    )
    geographic_scope = forms.ModelMultipleChoiceField(
        queryset=GeographicScope.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple(),
    )
    severity_pyramid_rung = forms.ModelMultipleChoiceField(
        queryset=SeverityPyramidRung.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple(),
    )
    from_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}), required=False
    )
    to_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}), required=False
    )
    signal_availability_days = forms.IntegerField(required=False)

    class Meta:
        model = Signal

        fields: list[str] = [
            "id",
            "pathogen",
            "active",
            "available_geographies",
            "severity_pyramid_rung",
            "source",
            "time_type",
            "geographic_scope",
            "from_date",
            "to_date",
            "signal_availability_days",
        ]

        widgets = {
            "available_geographies": forms.CheckboxSelectMultiple(
                attrs={
                    "class": "form-select",
                    "data-bs-toggle": "tooltip",
                    "data-bs-placement": "bottom",
                }
            ),
            "source": forms.CheckboxSelectMultiple(
                attrs={
                    "class": "form-select",
                    "data-bs-toggle": "tooltip",
                    "data-bs-placement": "bottom",
                }
            ),
            "time_type": forms.CheckboxSelectMultiple(
                attrs={
                    "class": "form-select",
                    "data-bs-toggle": "tooltip",
                    "data-bs-placement": "bottom",
                }
            ),
        }

    def __init__(self, *args, **kwargs) -> None:
        """
        Initialize the form.
        """
        super().__init__(*args, **kwargs)

        # Set required attribute to False and disable helptext for all fields
        self.fields["available_geographies"].queryset = self.fields[
            "available_geographies"
        ].queryset.order_by("display_order_number")
        try:
            self.fields["source"].choices = set(
                SourceSubdivision.objects.values_list("display_name", "display_name")
            )
            self.fields["time_type"].choices = set(Signal.objects.values_list("time_type", "time_type"))
        except (SourceSubdivision.DoesNotExist, Signal.DoesNotExist):
            self.fields["source"].choices = []
            self.fields["time_type"].choices = []
        for field_name, field in self.fields.items():
            field.required = False
            field.help_text = ""
            field.label = ""
        self.fields["from_date"].label = _("Available Since")
        self.fields["to_date"].label = _("Available Until")
        self.fields["signal_availability_days"].label = _(
            "Available for at least (days)"
        )
        self.fields["active"].label = _("Ongoing Surveillance Only")
