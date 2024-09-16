import logging

import django_filters
from django_filters.filters import (
    NumberFilter,
)

from django_filters.widgets import QueryArrayWidget

from datasources.models import SourceSubdivision
from signals.models import Signal

logger = logging.getLogger(__name__)


class SignalFilter(django_filters.FilterSet):
    id = NumberFilter(
        field_name="id",
        lookup_expr="in",
        widget=QueryArrayWidget,
    )
    source = django_filters.ModelMultipleChoiceFilter(
        queryset=SourceSubdivision.objects.all(),
        field_name="source_id__display_name",
        to_field_name="display_name",
    )

    class Meta:
        model = Signal
        fields: list[str] = [
            "id",
            "pathogen",
            "active",
            "source",
            "time_type",
            "geographic_scope",
            "severity_pyramid_rung",
            "from_date",
            "to_date",
            "signal_availability_days",
        ]
