import requests
import logging
from typing import Any
import json
from datetime import datetime as dtime

from django.conf import settings
from django.db.models.query import QuerySet
from django.views.generic import ListView
from django.http import JsonResponse


from signals.models import Geography, GeographyUnit
from signal_sets.models import SignalSet
from signal_sets.filters import SignalSetFilter
from signal_sets.forms import SignalSetFilterForm

from epiweeks import Week

logger = logging.getLogger(__name__)


class SignalSetListView(ListView):

    model = SignalSet
    template_name = "signal_sets/signal_sets.html"
    context_object_name = "signal_sets"

    def get_queryset(self) -> QuerySet[Any]:
        try:
            queryset = SignalSet.objects.all().prefetch_related(
                "geographic_scope",
                "data_source",
            )
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
        for signal in queryset.prefetch_related(
            "signal_set", "source", "severity_pyramid_rung"
        ):
            related_signals.append(
                {
                    "id": signal.id,
                    "display_name": signal.get_display_name,
                    "member_name": signal.member_name,
                    "name": signal.name,
                    "signal_set": signal.signal_set.id,
                    "signal_set_name": signal.signal_set.name,
                    "endpoint": signal.signal_set.endpoint,
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
        context["epidata_url"] = settings.EPIDATA_URL
        context["form"] = SignalSetFilterForm(initial=url_params_dict)
        context["filter"] = filter
        context["signal_sets"] = filter.qs
        context["related_signals"] = json.dumps(
            self.get_related_signals(filter.signals_qs)
        )
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


def epidata(request, endpoint=""):
    params = request.GET.dict()
    params["api_key"] = settings.EPIDATA_API_KEY
    url = f"{settings.EPIDATA_URL}{endpoint}"
    response = requests.get(url, params=params)
    return JsonResponse(response.json(), safe=False)


def get_epiweek(request):
    start_date = dtime.strptime(request.POST["start_date"], "%Y-%m-%d")
    start_date = Week.fromdate(start_date)
    end_date = dtime.strptime(request.POST["end_date"], "%Y-%m-%d")
    end_date = Week.fromdate(end_date)
    return JsonResponse(
        {
            "start_date": f"{start_date.year}{start_date.week if start_date.week >= 10 else '0' + str(start_date.week)}",
            "end_date": f"{end_date.year}{end_date.week if end_date.week >= 10 else '0' + str(end_date.week)}",
        }
    )
