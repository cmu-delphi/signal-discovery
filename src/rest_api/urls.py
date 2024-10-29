from django.urls import path
from django.urls.resolvers import URLPattern

from rest_api.views import api_signal_detail_view


urlpatterns: list[URLPattern] = [
    path("signal/<int:pk>", api_signal_detail_view, name="api_signal_detail"),
]
