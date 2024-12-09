from django.urls import path
from django.urls.resolvers import URLPattern

from rest_api.views import api_signal_detail_view, api_available_geography_view


urlpatterns: list[URLPattern] = [
    path("rest_api/signal/<int:pk>", api_signal_detail_view, name="api_signal_detail"),
    path("rest_api/signal/", api_signal_detail_view, name="api_signal_detail"),
    path("rest_api/geo_level/<int:pk>", api_available_geography_view, name="api_available_geography_detail"),
    path("rest_api/geo_level/", api_available_geography_view, name="api_available_geography_detail")
]
