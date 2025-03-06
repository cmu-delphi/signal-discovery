import logging

import django_filters
from django_filters.widgets import QueryArrayWidget
from django.db.models import Q

from signals.models import (
    Pathogen,
    GeographicScope,
    Geography,
    SeverityPyramidRung,
    Signal
)
from signal_sets.models import SignalSet
from datasources.models import DataSource
from signal_sets.utils import get_list_of_signals_filtered_by_geo

logger = logging.getLogger(__name__)


class SignalSetFilter(django_filters.FilterSet):

    signals_qs = Signal.objects.filter(signal_set__isnull=False)

    pathogens = django_filters.ModelMultipleChoiceFilter(
        field_name="pathogens",
        queryset=Pathogen.objects.filter(
            # id__in=SignalSet.objects.values_list("pathogens", flat="True")
            used_in="signal_sets"
        ),
        widget=QueryArrayWidget,
    )

    geographic_scope = django_filters.ModelMultipleChoiceFilter(
        field_name="geographic_scope",
        queryset=GeographicScope.objects.filter(
            # id__in=SignalSet.objects.values_list("geographic_scope", flat="True")
            used_in="signal_sets"
        ),
        widget=QueryArrayWidget,
    )

    available_geographies = django_filters.ModelMultipleChoiceFilter(
        field_name="available_geographies",
        queryset=Geography.objects.filter(
            # id__in=SignalSet.objects.values_list("available_geographies", flat="True")
            used_in="signal_sets"
        ).order_by("display_order_number"),
        widget=QueryArrayWidget,
    )

    severity_pyramid_rungs = django_filters.ModelMultipleChoiceFilter(
        field_name="severity_pyramid_rungs",
        queryset=SeverityPyramidRung.objects.filter(
            # id__in=SignalSet.objects.values_list("severity_pyramid_rungs", flat="True")
            used_in="signal_sets"
        ),
        widget=QueryArrayWidget,
    )

    data_source = django_filters.ModelMultipleChoiceFilter(
        field_name="data_source",
        queryset=DataSource.objects.filter(
            id__in=SignalSet.objects.values_list("data_source", flat="True")
        ),
        widget=QueryArrayWidget,
    )

    temporal_granularity = django_filters.MultipleChoiceFilter(
        field_name="temporal_granularity",
        choices=[
            ("Annually", "Annually"),
            ("Monthly", "Monthly"),
            ("Weekly", "Weekly"),
            ("Daily", "Daily"),
            ("Hourly", "Hourly"),
            ("Other", "Other"),
        ],
        lookup_expr="icontains",
    )

    temporal_scope_end = django_filters.MultipleChoiceFilter(
        field_name="temporal_scope_end",
        choices=[
            ("Ongoing", "Ongoing Surveillance Only"),
        ],
    )

    location_search = django_filters.CharFilter(
        method="filter_by_geo",
        widget=QueryArrayWidget,
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
            "temporal_scope_end",
        ]

    def filter_by_geo(self, queryset, name, value):
        if not value:
            return queryset
        filtered_signals = get_list_of_signals_filtered_by_geo(value)
        query = Q()
        for item in filtered_signals["epidata"]:
            query |= Q(source__name=item["source"], name=item["signal"])
        self.signals_qs = self.signals_qs.filter(query)
        signal_sets = self.signals_qs.values_list("signal_set_id", flat=True).distinct()
        return queryset.filter(id__in=signal_sets)
