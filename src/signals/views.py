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

    model = SignalsDbView
    template_name = "signals/signals.html"
    context_object_name = "signals"

    def get_queryset(self) -> QuerySet[Any]:
        try:
            queryset = SignalsDbView.objects.all()
            if self.request.GET.getlist("id"):
                queryset = queryset.filter(id__in=self.request.GET.getlist("id"))
            f = SignalFilter(self.request.GET, queryset=queryset)
            return f.qs
        except Exception as e:
            logger.error(f"Error getting queryset: {e}")
            return SignalsDbView.objects.none()

    def get_url_params(self):
        url_params_dict = {
            "id": [int(el) for el in self.request.GET.getlist("id")] if self.request.GET.getlist("id") else None,
            "search": self.request.GET.get("search"),
            "pathogens": [int(el) for el in self.request.GET.getlist("pathogens")],
            "active": [el for el in self.request.GET.getlist("active")],
            "available_geography": (
                [int(el) for el in self.request.GET.getlist("available_geography")]
                if self.request.GET.get("available_geography")
                else None
            ),
            "severity_pyramid_rung": (
                [el for el in self.request.GET.getlist("severity_pyramid_rung")]
                if self.request.GET.get("severity_pyramid_rung")
                else None
            ),
            "geographic_scope": (
                [el for el in self.request.GET.getlist("geographic_scope")]
                if self.request.GET.get("geographic_scope")
                else None
            ),
            "datasource": [el for el in self.request.GET.getlist("datasource")],
            "time_type": [el for el in self.request.GET.getlist("time_type")],
            "from_date": self.request.GET.get("from_date"),
            "to_date": self.request.GET.get("to_date"),
            "signal_availability_days": self.request.GET.get(
                "signal_availability_days"
            ),
        }
        url_params_str = ""
        for param_name, param_value in url_params_dict.items():
            if isinstance(param_value, list):
                for value in param_value:
                    url_params_str = f"{url_params_str}&{param_name}={value}"
            else:
                if param_value not in ["", None]:
                    url_params_str = f"{url_params_str}&{param_name}={param_value}"
        return url_params_dict, url_params_str

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        url_params_dict, url_params_str = self.get_url_params()
        context["url_params_dict"] = url_params_dict
        context["url_params_str"] = url_params_str
        context["form"] = SignalFilterForm(initial=url_params_dict)
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
        context["epidata_url"] = settings.EPIDATA_URL
        return context
