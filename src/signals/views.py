from typing import Any, Dict
import logging

from django.conf import settings
from django.db.models.query import QuerySet
from django.views.generic import DetailView, ListView


from signals.filters import SignalFilter
from signals.forms import SignalFilterForm
from signals.models import Signal, SignalsDbView


logger = logging.getLogger(__name__)


class SignalsListView(ListView):
    """
    ListView for displaying a list of Signal objects.
    """

    model = Signal
    template_name = "signals/signals.html"
    context_object_name = "signals"

    def get_queryset(self) -> QuerySet[Any]:
        try:
            queryset = SignalsDbView.objects.all()
            f = SignalFilter(self.request.GET, queryset=queryset)
            return f.qs
        except Exception as e:
            logger.error(f"Error getting queryset: {e}")
            return SignalsDbView.objects.none()

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["form"] = SignalFilterForm()
        context["filter"] = SignalFilter(self.request.GET, queryset=self.get_queryset())
        context["signals"] = self.get_queryset()

        return context


class SignalsDetailView(DetailView):
    """
    DetailView for displaying a single Signal object.
    """

    model = Signal

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        """
        Get the context data for the view.

        Returns:
            Dict[str, Any]: The context data for the view.
        """

        context: Dict[str, Any] = super().get_context_data(**kwargs)
        context["epivis_url"] = settings.EPIVIS_URL
        context["data_export_url"] = settings.DATA_EXPORT_URL
        context["covidcast_url"] = settings.COVIDCAST_URL
        return context
