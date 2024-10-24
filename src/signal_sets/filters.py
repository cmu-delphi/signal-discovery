import logging

import django_filters
from django_filters.widgets import QueryArrayWidget

from signals.models import Pathogen, GeographicScope, Geography, SeverityPyramidRung
from signal_sets.models import SignalSet
from datasources.models import DataSource

logger = logging.getLogger(__name__)


class SignalSetFilter(django_filters.FilterSet):

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

    available_geographies = django_filters.ModelMultipleChoiceFilter(
        field_name="available_geographies",
        queryset=Geography.objects.all().order_by("display_order_number"),
        widget=QueryArrayWidget,
    )

    severity_pyramid_rungs = django_filters.ModelMultipleChoiceFilter(
        field_name="severity_pyramid_rungs",
        queryset=SeverityPyramidRung.objects.all(),
        widget=QueryArrayWidget,
    )

    data_source = django_filters.ModelMultipleChoiceFilter(
        field_name="data_source",
        queryset=DataSource.objects.all(),
        widget=QueryArrayWidget,
    )

    temporal_granularity = django_filters.MultipleChoiceFilter(
        field_name="temporal_granularity",
        choices=[
            ("Daily", "Daily"),
            ("Weekly", "Weekly"),
            ("Hourly", "Hourly"),
        ],
        lookup_expr="icontains",
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
