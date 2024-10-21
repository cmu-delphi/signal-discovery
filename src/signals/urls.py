from django.urls import path
from django.urls.resolvers import URLPattern

from signals.views import (
    SignalsDetailView,
    SignalsListView,
)


urlpatterns: list[URLPattern] = [
    path("", SignalsListView.as_view(), name="signals"),
    path("/signal/<int:pk>/", SignalsDetailView.as_view(), name="signal"),
    path("/signal/<pk>/", SignalsDetailView.as_view(), name="signal"),
]
