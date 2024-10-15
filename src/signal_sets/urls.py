from django.urls import path
from django.urls.resolvers import URLPattern

from signal_sets.views import SignalSetDetailedView, SignalSetListView

urlpatterns: list[URLPattern] = [
    path("", SignalSetListView.as_view(), name="signal_sets"),
    path("signal_sets/<int:pk>/", SignalSetDetailedView.as_view(), name="signal_set"),
    path("signal_sets/<pk>/", SignalSetDetailedView.as_view(), name="signal_set"),
]
