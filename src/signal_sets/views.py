import logging
from typing import Any, Dict

from django.db.models.query import QuerySet
from django.views.generic import ListView, DetailView

from signal_sets.models import SignalSet
from signal_sets.filters import SignalSetFilter
from signal_sets.forms import SignalSetFilterForm

logger = logging.getLogger(__name__)


class SignalSetListView(ListView):

    model = SignalSet
    template_name = "signal_sets/signal_sets.html"
    context_object_name = "signal_sets"

    def get_queryset(self) -> QuerySet[Any]:
        try:
            queryset = SignalSet.objects.all()
            f = SignalSetFilter(self.request.GET, queryset=queryset)
            return f.qs
        except Exception as e:
            logger.error(f"Error getting queryset: {e}")
            return SignalSet.objects.none()

    def get_url_params(self):
        url_params_dict = {
            "pathogens": [int(el) for el in self.request.GET.getlist("pathogens")],
            "geographic_scope": (
                [el for el in self.request.GET.getlist("geographic_scope")]
                if self.request.GET.get("geographic_scope")
                else None
            ),
            "severity_pyramid_rungs": (
                [el for el in self.request.GET.getlist("severity_pyramid_rungs")]
                if self.request.GET.get("severity_pyramid_rungs")
                else None
            ),
            "data_source": [el for el in self.request.GET.getlist("data_source")],
            "temporal_granularity": [el for el in self.request.GET.getlist("temporal_granularity")],
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

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        url_params_dict, url_params_str = self.get_url_params()
        context["url_params_dict"] = url_params_dict
        context["url_params_str"] = url_params_str
        context["form"] = SignalSetFilterForm(initial=url_params_dict)
        context["filter"] = SignalSetFilter(
            self.request.GET, queryset=self.get_queryset()
        )
        context["signal_sets"] = self.get_queryset()
        return context


class SignalSetDetailedView(DetailView):

    model = SignalSet
    template_name = "signal_sets/signal_set_detail.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: Dict[str, Any] = super().get_context_data(**kwargs)
        return context
