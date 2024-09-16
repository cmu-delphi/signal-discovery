from django.urls import path
from django.urls.resolvers import URLPattern
from django.views.decorators.cache import cache_page

from signals.views import (
    SignalsDetailView,
    SignalsListView,
)


urlpatterns: list[URLPattern] = [
    path("", SignalsListView.as_view(), name="signals"),
    path("signals/<int:pk>/", SignalsDetailView.as_view(), name="signal"),
    path("signals/<pk>/", SignalsDetailView.as_view(), name="signal"),
]
