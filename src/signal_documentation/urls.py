"""
URL configuration for signal_documentation project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from base.views import (
    BadRequestErrorView,
    ForbiddenErrorView,
    InternalServerErrorView,
    NotFoundErrorView,
)

handler400 = BadRequestErrorView.as_view()
handler403 = ForbiddenErrorView.as_view()
handler404 = NotFoundErrorView.as_view()
handler500 = InternalServerErrorView.as_view()


urlpatterns = [
    path(f'{settings.MAIN_PAGE}/admin/' if settings.MAIN_PAGE else 'admin/', admin.site.urls),
    # signal_sets
    path(
        f"{settings.MAIN_PAGE}/" if settings.MAIN_PAGE else "",
        include("signal_sets.urls"),
    ),
    # signals
    path(
        f"{settings.MAIN_PAGE}/signals/" if settings.MAIN_PAGE else "signals/",
        include("signals.urls"),
    ),
    # datasources
    path(
        f"{settings.MAIN_PAGE}/datasources/" if settings.MAIN_PAGE else "datasources/",
        include("datasources.urls"),
    ),
    # rest_api
    path(
        f"{settings.MAIN_PAGE}/rest_api/" if settings.MAIN_PAGE else "rest_api/",
        include("rest_api.urls"),
    ),
    path("__debug__/", include("debug_toolbar.urls")),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # type: ignore
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # type: ignore
