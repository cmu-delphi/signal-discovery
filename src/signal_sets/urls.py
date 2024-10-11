from django.urls import path
from django.urls.resolvers import URLPattern

from signal_sets.views import SignalSetListView

urlpatterns: list[URLPattern] = [
    path("", SignalSetListView.as_view(), name="signal_sets"),
    # path("signals/<int:pk>/", SignalsDetailView.as_view(), name="signal"),
    # path("signals/<pk>/", SignalsDetailView.as_view(), name="signal"),
]