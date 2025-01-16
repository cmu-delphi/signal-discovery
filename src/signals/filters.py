import logging

import django_filters
from django.db.models import Q
import ast
from django_filters.widgets import BooleanWidget, QueryArrayWidget

from signals.models import (
    Pathogen,
    GeographicScope,
    Geography,
    SignalsDbView,
    SeverityPyramidRung,
    Signal
)
from datasources.models import SourceSubdivision

logger = logging.getLogger(__name__)


class SignalFilter(django_filters.FilterSet):
    active = django_filters.BooleanFilter(
        field_name="active",
        widget=BooleanWidget(),
    )

    pathogens = django_filters.CharFilter(
        method="filter_pathogens", widget=QueryArrayWidget
    )

    geographic_scope = django_filters.CharFilter(
        method="filter_geographic_scope", widget=QueryArrayWidget
    )

    available_geography = django_filters.CharFilter(
        method="filter_available_geography",
        widget=QueryArrayWidget,
    )

    severity_pyramid_rung = django_filters.CharFilter(
        method="filter_severity_pyramid_rung",
        widget=QueryArrayWidget,
    )

    datasource = django_filters.ModelMultipleChoiceFilter(
        queryset=SourceSubdivision.objects.filter(id__in=Signal.objects.values_list("source", flat=True)),
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

    def filter_pathogens(self, queryset, name, value):
        if not value:
            return queryset
        pathogens = list(
            Pathogen.objects.filter(
                id__in=ast.literal_eval(value)
            ).values_list("name", flat=True)
        )
        queries: list[Q] = [Q((f"{name}__icontains", p)) for p in pathogens]
        query: Q = queries.pop()

        for item in queries:
            query |= item

        return queryset.filter(query)

    def filter_geographic_scope(self, queryset, name, value):
        if not value:
            return queryset
        geographic_scopes = list(
            GeographicScope.objects.filter(id__in=ast.literal_eval(value)).values_list(
                "name", flat=True
            )
        )
        queries: list[Q] = [Q((f"{name}__icontains", g)) for g in geographic_scopes]
        query: Q = queries.pop()

        for item in queries:
            query |= item

        return queryset.filter(query)

    def filter_available_geography(self, queryset, name, value):
        if not value:
            return queryset
        available_geography = list(
            Geography.objects.filter(id__in=ast.literal_eval(value)).values_list(
                "name", flat=True
            )
        )
        queries: list[Q] = [Q((f"{name}__icontains", ag)) for ag in available_geography]
        query: Q = queries.pop()

        for item in queries:
            query |= item

        return queryset.filter(query)

    def filter_severity_pyramid_rung(self, queryset, name, value):
        if not value:
            return queryset
        severity_pyramid_rungs = list(
            SeverityPyramidRung.objects.filter(
                id__in=ast.literal_eval(value)
            ).values_list("name", flat=True)
        )
        queries: list[Q] = [
            Q((f"{name}__icontains", s)) for s in severity_pyramid_rungs
        ]
        query: Q = queries.pop()

        for item in queries:
            query |= item

        return queryset.filter(query)
