import logging
from typing import Any

from django.db.models.query import QuerySet
from django.views.generic import ListView

from signal_sets.models import SignalSet

logger = logging.getLogger(__name__)


class SignalSetListView(ListView):

    model = SignalSet
    template_name = "signal_sets/signal_sets.html"
    context_object_name = "signal_sets"

    def get_queryset(self) -> QuerySet[Any]:
        try:
            queryset = SignalSet.objects.all()
            return queryset
        except Exception as e:
            logger.error(f"Error getting queryset: {e}")
            return SignalSet.objects.none()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["signal_sets"] = self.get_queryset()

        return context
