import logging

import django_filters
from django_filters.filters import NumberFilter
from django_filters.widgets import BooleanWidget, QueryArrayWidget

from signals.models import Pathogen, GeographicScope, Geography, SignalsDbView, SeverityPyramidRung

logger = logging.getLogger(__name__)


class SignalFilter(django_filters.FilterSet):
    id = NumberFilter(
        field_name="id",
        lookup_expr="in",
        widget=QueryArrayWidget,
    )

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

    available_geographies = django_filters.ModelMultipleChoiceFilter(
        field_name="available_geographies",
        queryset=Geography.objects.all().order_by("display_order_number"),
        widget=QueryArrayWidget,
    )

    severity_pyramid_rung = django_filters.ModelMultipleChoiceFilter(
        field_name="severity_pyramid_rung",
        queryset=SeverityPyramidRung.objects.all(),
        widget=QueryArrayWidget,
    )

    class Meta:
        model = SignalsDbView
        fields: list[str] = ["id", "active", "pathogens", "geographic_scope"]
