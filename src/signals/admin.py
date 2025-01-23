from typing import Literal

from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from signals.resources import SignalResource, SignalBaseResource


from signals.models import (
    Category,
    FormatType,
    GeographicScope,
    Geography,
    Pathogen,
    SeverityPyramidRung,
    Signal,
    SignalType,
    SignalGeography,
)


@admin.register(Category)
class SignalCategoryAdmin(admin.ModelAdmin):
    """
    Admin interface for managing signal category objects.
    """
    list_display: tuple[Literal['name'], Literal['display_name']] = ('name', 'display_name')
    search_fields: tuple[Literal['name']] = ('name',)


@admin.register(FormatType)
class FormatTypeAdmin(admin.ModelAdmin):
    """
    Admin interface for managing format type objects.
    """
    list_display: tuple[Literal['name'], Literal['display_name']] = ('name', 'display_name')
    search_fields: tuple[Literal['name']] = ('name',)


@admin.register(GeographicScope)
class GeographicScopeAdmin(admin.ModelAdmin):
    """
    Admin interface for managing geographic scope objects.
    """
    list_display: tuple[Literal['name'], Literal['display_name']] = ('name', 'used_in')
    search_fields: tuple[Literal['name']] = ('name', 'used_in')


@admin.register(Geography)
class GeographyAdmin(admin.ModelAdmin):
    """
    Admin interface for managing geography objects.
    """
    list_display: tuple[Literal['name'], Literal['display_name']] = ('name', 'display_name')
    search_fields: tuple[Literal['name']] = ('name',)


@admin.register(Pathogen)
class PathogenAdmin(admin.ModelAdmin):
    """
    Admin interface for managing pathogen objects.
    """
    list_display: tuple[Literal['name']] = ('name', 'used_in')
    search_fields: tuple[Literal['name']] = ('name', 'used_in')


@admin.register(SeverityPyramidRung)
class SeverityPyramidRungAdmin(admin.ModelAdmin):
    """
    Admin interface for managing severity pyramid objects.
    """
    list_display: tuple[Literal['name'], Literal['display_name']] = ('name', 'display_name', 'used_in',)
    search_fields: tuple[Literal['name']] = ('name',)


@admin.register(SignalType)
class SignalTypeAdmin(admin.ModelAdmin):
    """
    Admin interface for managing signal type objects.
    """
    list_display: tuple[Literal['name'], Literal['display_name']] = ('name', 'display_name')
    search_fields: tuple[Literal['name']] = ('name',)


@admin.register(Signal)
class SignalAdmin(ImportExportModelAdmin):
    """
    Admin interface for managing signal objects.
    """
    list_display: tuple[Literal['name'], Literal['signal_type'], Literal['format_type'], Literal['category'], Literal[
        'geographic_scope']] = (
        'name', 'signal_type', 'format_type', 'category', 'geographic_scope')
    search_fields: tuple[
        Literal['name'], Literal['signal_type__name'], Literal['format_type__name'], Literal['category__name'], Literal[
            'geographic_scope__name']] = (
        'name', 'signal_type__name', 'format_type__name', 'category__name', 'geographic_scope__name')
    resource_classes: list[type[SignalResource]] = [SignalResource, SignalBaseResource]


@admin.register(SignalGeography)
class SignalGeographyAdmin(admin.ModelAdmin):
    """
    Admin interface for managing signal category objects.
    """
    list_display: tuple[Literal['geography'], Literal['signal'], Literal['aggregated_by_delphi']] = ('geography', 'signal', 'aggregated_by_delphi')
    search_fields: tuple[Literal['name']] = ('geography', 'signal')