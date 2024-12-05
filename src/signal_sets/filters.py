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
        queryset=Pathogen.objects.filter(id__in=SignalSet.objects.values_list("pathogens", flat="True")),
        widget=QueryArrayWidget,
    )

    geographic_scope = django_filters.ModelMultipleChoiceFilter(
        field_name="geographic_scope",
        queryset=GeographicScope.objects.filter(id__in=SignalSet.objects.values_list("geographic_scope", flat="True")),
        widget=QueryArrayWidget,
    )

    available_geographies = django_filters.ModelMultipleChoiceFilter(
        field_name="available_geographies",
        queryset=Geography.objects.filter(id__in=SignalSet.objects.values_list("available_geographies", flat="True")).order_by("display_order_number"),
        widget=QueryArrayWidget,
    )

    severity_pyramid_rungs = django_filters.ModelMultipleChoiceFilter(
        field_name="severity_pyramid_rungs",
        queryset=SeverityPyramidRung.objects.filter(id__in=SignalSet.objects.values_list("severity_pyramid_rungs", flat="True")),
        widget=QueryArrayWidget,
    )

    data_source = django_filters.ModelMultipleChoiceFilter(
        field_name="data_source",
        queryset=DataSource.objects.filter(id__in=SignalSet.objects.values_list("data_source", flat="True")),
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
