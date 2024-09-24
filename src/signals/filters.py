import logging

import django_filters
from django_filters.widgets import BooleanWidget, QueryArrayWidget

from signals.models import (
    Pathogen,
    GeographicScope,
    Geography,
    SignalsDbView,
    SeverityPyramidRung,
)
from datasources.models import SourceSubdivision

logger = logging.getLogger(__name__)


class SignalFilter(django_filters.FilterSet):
    active = django_filters.BooleanFilter(
        field_name="active",
        widget=BooleanWidget(),
    )

    pathogens = django_filters.ModelMultipleChoiceFilter(
        field_name="pathogens",
        queryset=Pathogen.objects.all(),
        widget=QueryArrayWidget,
    )

    geographic_scope = django_filters.ModelMultipleChoiceFilter(
        field_name="geographic_scope",
        queryset=GeographicScope.objects.all(),
        widget=QueryArrayWidget,
    )

    available_geography = django_filters.ModelMultipleChoiceFilter(
        field_name="available_geography",
        queryset=Geography.objects.all().order_by("display_order_number"),
        widget=QueryArrayWidget,
    )

    severity_pyramid_rung = django_filters.ModelMultipleChoiceFilter(
        field_name="severity_pyramid_rung",
        queryset=SeverityPyramidRung.objects.all(),
        widget=QueryArrayWidget,
    )

    datasource = django_filters.ModelMultipleChoiceFilter(
        queryset=SourceSubdivision.objects.all(),
        field_name="datasource",
        to_field_name="display_name",
    )

    time_type = django_filters.MultipleChoiceFilter(
        field_name="time_type",
        choices=[
            ("day", "Day"),
            ("week", "Week"),
        ],
    )

    from_date = django_filters.DateFilter(
        field_name="from_date",
        lookup_expr="gte",
    )

    to_date = django_filters.DateFilter(
        field_name="to_date",
        lookup_expr="lte",
    )

    signal_availability_days = django_filters.NumberFilter(
        field_name="signal_availability_days",
        lookup_expr="gte",
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
