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
            queryset = SignalSet.objects.all().prefetch_related("geographic_scope", "data_source", )
            return queryset
        except Exception as e:
            logger.error(f"Error getting queryset: {e}")
            return SignalSet.objects.none()

    def get_url_params(self):
        url_params_dict = {
            "pathogens": (
                [int(el) for el in self.request.GET.getlist("pathogens")]
                if self.request.GET.get("pathogens")
                else ""
            ),
            "geographic_scope": (
                [el for el in self.request.GET.getlist("geographic_scope")]
                if self.request.GET.get("geographic_scope")
                else ""
            ),
            "severity_pyramid_rungs": (
                [el for el in self.request.GET.getlist("severity_pyramid_rungs")]
                if self.request.GET.get("severity_pyramid_rungs")
                else ""
            ),
            "data_source": [el for el in self.request.GET.getlist("data_source")],
            "temporal_granularity": (
                [el for el in self.request.GET.getlist("temporal_granularity")]
                if self.request.GET.get("temporal_granularity")
                else ""
            ),
            "available_geographies": (
                [el for el in self.request.GET.getlist("available_geographies")]
                if self.request.GET.get("available_geographies")
                else ""
            ),
            "temporal_scope_end": (
                self.request.GET.get("temporal_scope_end")
                if self.request.GET.get("temporal_scope_end")
                else ""
            ),
            "location_search": (
                [el for el in self.request.GET.getlist("location_search")]
                if self.request.GET.get("location_search")
                else ""
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

    def get_related_signals(self, queryset):
        related_signals = []
        for signal_set in queryset:
            for signal in signal_set.signals.all().prefetch_related("signal_set", "source", "severity_pyramid_rung"):
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
                        "description": signal.description,
                    }
                )
        return related_signals

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        url_params_dict, url_params_str = self.get_url_params()
        filter = SignalSetFilter(self.request.GET, queryset=queryset)
        context["url_params_dict"] = url_params_dict
        context["url_params_str"] = url_params_str
        context["epivis_url"] = settings.EPIVIS_URL
        context["data_export_url"] = settings.DATA_EXPORT_URL
        context["covidcast_url"] = settings.COVIDCAST_URL
        context["form"] = SignalSetFilterForm(initial=url_params_dict)
        context["filter"] = filter
        context["signal_sets"] = filter.qs
        context["related_signals"] = json.dumps(self.get_related_signals(filter.qs))
        context["available_geographies"] = Geography.objects.filter(used_in="signals")
        context["geographic_granularities"] = [
            {
                "id": str(geo_unit.geo_id),
                "geoType": geo_unit.geography.name,
                "text": geo_unit.display_name,
            }
            for geo_unit in GeographyUnit.objects.all().prefetch_related("geography")
        ]
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
