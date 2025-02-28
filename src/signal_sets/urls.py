from django.urls import path, re_path
from django.urls.resolvers import URLPattern

from signal_sets.views import SignalSetListView, epidata, get_epiweek

urlpatterns: list[URLPattern] = [
    path("", SignalSetListView.as_view(), name="signal_sets"),
    re_path(r'^epidata/(?P<endpoint>.*)/$', epidata, name="epidata"),
    path("get_epiweek/", get_epiweek, name="get_epiweek"),
]
