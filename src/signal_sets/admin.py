from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from signal_sets.resources import SignalSetResource
from signal_sets.models import SignalSet


@admin.register(SignalSet)
class SignalSetAdmin(ImportExportModelAdmin):
    list_display = ('name', 'description', 'maintainer_name', 'maintainer_email', 'organization')
    search_fields = ('name', 'maintainer_name', 'maintainer_email', 'organization')
    resource_class = SignalSetResource
