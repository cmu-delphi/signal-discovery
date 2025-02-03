import logging
from typing import Any, Dict
import json

from django.conf import settings
from django.db.models.query import QuerySet
from django.views.generic import ListView, DetailView


from signals.models import Geography, GeographyUnit
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
            "temporal_granularity": [
                el for el in self.request.GET.getlist("temporal_granularity")
            ],
            "available_geographies": (
                [el for el in self.request.GET.getlist("available_geographies")]
                if self.request.GET.get("available_geographies")
                else None
            ),
            "temporal_scope_end": self.request.GET.get("temporal_scope_end"),
            "location_search": (
                [el for el in self.request.GET.getlist("location_search")]
                if self.request.GET.get("location_search")
                else None
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

    def get_related_signals(self):
        related_signals = []
        for signal_set in self.get_queryset():
            for signal in signal_set.signals.all():
                related_signals.append(
                    {
                        "id": signal.id,
                        "display_name": signal.get_display_name,
                        "name": signal.name,
                        "signal_set": signal_set.id,
                        "signal_set_name": signal_set.name,
                        "endpoint": signal_set.endpoint,
                        "source": signal.source.name,
                        "time_type": signal.time_type,
                        "description": signal.description
                    }
                )
        return related_signals

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        url_params_dict, url_params_str = self.get_url_params()
        context["url_params_dict"] = url_params_dict
        context["url_params_str"] = url_params_str
        context["epivis_url"] = settings.EPIVIS_URL
        context["data_export_url"] = settings.DATA_EXPORT_URL
        context["covidcast_url"] = settings.COVIDCAST_URL
        context["form"] = SignalSetFilterForm(initial=url_params_dict)
        context["filter"] = SignalSetFilter(
            self.request.GET, queryset=self.get_queryset()
        )
        context["signal_sets"] = self.get_queryset()
        context["related_signals"] = json.dumps(self.get_related_signals())
        context["available_geographies"] = Geography.objects.filter(used_in="signals")
        context["geographic_granularities"] = [{"id": str(geo_unit.geo_id), "geoType": geo_unit.geography.name, "text": geo_unit.display_name} for geo_unit in GeographyUnit.objects.all()]
        return context


class SignalSetDetailedView(DetailView):

    model = SignalSet
    template_name = "signal_sets/signal_set_detail.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: Dict[str, Any] = super().get_context_data(**kwargs)
        context["epivis_url"] = settings.EPIVIS_URL
        context["data_export_url"] = settings.DATA_EXPORT_URL
        context["covidcast_url"] = settings.COVIDCAST_URL
        context["data_source"] = (
            self.object.signals.all()
            .values_list("source__name", flat=True)
            .distinct()
            .order_by()
            .first()
        )
        context["available_geographies"] = Geography.objects.filter(
            id__in=self.object.signals.all()
            .values_list("available_geography")
            .distinct()
            .order_by()
        )
        context["time_type"] = (
            self.object.signals.all()
            .values_list("time_type", flat=True)
            .distinct()
            .order_by()
            .first()
        )

        return context
