from typing import Any
from django.db import IntegrityError, transaction
from django.db.models import Max


from import_export import resources
from import_export.fields import Field, widgets

from datasources.models import DataSource
from signal_sets.models import SignalSet
from signals.models import GeographicScope, Geography, Pathogen, SeverityPyramidRung


def process_pathogens(row) -> None:
    """
    Processes pathogen.
    """
    if row["Pathogen(s)/Syndrome(s)"]:
        pathogens = row["Pathogen(s)/Syndrome(s)"].split(",")
        for pathogen in pathogens:
            pathogen = pathogen.strip()
            pathogen_obj, _ = Pathogen.objects.get_or_create(name=pathogen, used_in="signal_sets")


def process_geographic_scope(row) -> None:
    """
    Processes geographic scope.
    """
    if row["Geographic Coverage"]:
        geographic_scope = row["Geographic Coverage"]
        geographic_scope_obj, _ = GeographicScope.objects.get_or_create(
            name=geographic_scope, used_in="signal_sets"
        )
        row["Geographic Coverage"] = geographic_scope_obj.id


def process_severity_pyramid_rungs(row) -> None:
    """
    Processes pathogen.
    """
    if row["Surveillance Categories"]:
        severity_pyramid_rungs = row["Surveillance Categories"].split(",")
        for severity_pyramid_rung in severity_pyramid_rungs:
            severity_pyramid_rung = severity_pyramid_rung.strip()
            severity_pyramid_rung_obj, _ = SeverityPyramidRung.objects.get_or_create(
                name=severity_pyramid_rung,
                used_in="signal_sets",
                defaults={"used_in": "signal_sets", "display_name": severity_pyramid_rung}
            )


def process_avaliable_geographies(row) -> None:
    if row["Geographic Granularity - Delphi"]:
        available_geographies = row["Geographic Granularity - Delphi"].split(",")
        for available_geography in available_geographies:
            max_display_order_number = Geography.objects.filter(used_in="signals").aggregate(Max("display_order_number"))["display_order_number__max"]
            available_geography_obj, _ = Geography.objects.get_or_create(
                name=available_geography,
                used_in="signal_sets",
                defaults={"used_in": "signal_sets", "display_order_number": max_display_order_number + 1}
            )


def process_datasources(row) -> None:
    """
    Processes data source.
    """
    if row["Original Data Provider"]:
        data_source = row["Original Data Provider"]
        data_source_obj, _ = DataSource.objects.get_or_create(name=data_source, defaults={"display_name": data_source.capitalize()})
        row["Original Data Provider"] = data_source_obj


def fix_boolean_fields(row) -> Any:
    """
    Fixes boolean fields.
    """
    fields = [
        "Include in indicator app",
    ]
    for k in fields:
        if row[k] == "TRUE":
            row[k] = True
        if row[k] == "FALSE" or row[k] == "":
            row[k] = False
    return row


class SignalSetResource(resources.ModelResource):

    name = Field(attribute="name", column_name="Indicator Set name* ")
    short_name = Field(attribute="short_name", column_name="Indicator Set Short Name")
    description = Field(attribute="description", column_name="Indicator Set Description*")
    maintainer_name = Field(
        attribute="maintainer_name", column_name="Maintainer/\nKey Contact *"
    )
    maintainer_email = Field(
        attribute="maintainer_email", column_name="Email of maintainer/\nkey contact *"
    )
    organization = Field(attribute="organization", column_name="Organization")
    data_source = Field(
        attribute="data_source",
        column_name="Original Data Provider",
        widget=widgets.ForeignKeyWidget(DataSource, field="name"),
    )
    endpoint = Field(attribute="endpoint", column_name="Endpoint")
    language = Field(attribute="language", column_name="Language (likely English) ")
    version_number = Field(
        attribute="version_number", column_name="Version Number \n(if applicable) "
    )
    origin_datasource = Field(
        attribute="origin_datasource",
        column_name="Source dataset from which data was derived (for aggregates or processed data) ",
    )
    data_type = Field(attribute="data_type", column_name="Type(s) of Data*")
    geographic_scope = Field(
        attribute="geographic_scope",
        column_name="Geographic Coverage",
        widget=widgets.ForeignKeyWidget(GeographicScope),
    )
    geographic_granularity = Field(
        attribute="geographic_granularity",
        column_name="Geographic Levels",
    )
    preprocessing_description = Field(
        attribute="preprocessing_description",
        column_name="Pre-processing",
    )
    temporal_scope_start = Field(
        attribute="temporal_scope_start", column_name="Temporal Scope Start"
    )
    temporal_scope_end = Field(
        attribute="temporal_scope_end", column_name="Temporal Scope End"
    )
    temporal_granularity = Field(
        attribute="temporal_granularity", column_name="Temporal Granularity"
    )
    reporting_cadence = Field(
        attribute="reporting_cadence", column_name="Reporting Cadence"
    )
    reporting_lag = Field(
        attribute="reporting_lag", column_name="Reporting Lag (nominal)"
    )
    demographic_scope = Field(
        attribute="demographic_scope", column_name="Population"
    )
    revision_cadence = Field(
        attribute="revision_cadence", column_name="Revision Cadence"
    )
    demographic_granularity = Field(
        attribute="demographic_granularity", column_name="Population Stratifiers"
    )
    censoring = Field(attribute="censoring", column_name="Censoring")
    missingness = Field(attribute="missingness", column_name="Missingness")
    dua_required = Field(attribute="dua_required", column_name="DUA required?")
    license = Field(attribute="license", column_name="Data Use Terms")
    dataset_location = Field(
        attribute="dataset_location", column_name="Dataset Location"
    )
    link_to_documentation = Field(
        attribute="link_to_documentation", column_name="Link to documentation"
    )

    class Meta:
        model = SignalSet
        fields: list[str] = [
            "name",
            "short_name",
            "description",
            "maintainer_name",
            "maintainer_email",
            "organization",
            "data_source",
            "language",
            "version_number",
            "origin_datasource",
            "data_type",
            "geographic_scope",
            "geographic_granularity",
            "preprocessing_description",
            "temporal_scope_start",
            "temporal_scope_end",
            "temporal_granularity",
            "reporting_cadence",
            "reporting_lag",
            "demographic_scope",
            "revision_cadence",
            "demographic_granularity",
            "censoring",
            "missingness",
            "dua_required",
            "license",
            "dataset_location",
            "link_to_documentation",
            "endpoint",
            "available_geographies",
        ]
        import_id_fields = ["name", "data_source"]
        store_instance = True
        skip_unchanged = True

    def before_import_row(self, row, **kwargs):
        fix_boolean_fields(row)
        process_pathogens(row)
        process_severity_pyramid_rungs(row)
        process_geographic_scope(row)
        process_avaliable_geographies(row)
        process_datasources(row)

    def save_instance(self, instance, is_create, row, **kwargs):
        try:
            with transaction.atomic():
                return super().save_instance(instance, is_create, row, **kwargs)
        except IntegrityError:
            pass

    def skip_row(self, instance, original, row, import_validation_errors=None):
        if not row["Include in indicator app"]:
            return True

    def after_import_row(self, row, row_result, **kwargs):
        try:
            signal_set_obj = SignalSet.objects.get(id=row_result.object_id)
            signal_set_obj.pathogens.clear()
            signal_set_obj.severity_pyramid_rungs.clear()
            signal_set_obj.available_geographies.clear()
            for pathogen in row["Pathogen(s)/Syndrome(s)"].split(","):
                pathogen = Pathogen.objects.get(name=pathogen, used_in="signal_sets")
                signal_set_obj.pathogens.add(pathogen)
            for severity_pyramid_rung in row["Surveillance Categories"].split(","):
                severity_pyramid_rung = SeverityPyramidRung.objects.filter(
                    name=severity_pyramid_rung,
                    used_in="signal_sets"
                ).first()
                signal_set_obj.severity_pyramid_rungs.add(severity_pyramid_rung)
            for available_geography in row["Geographic Granularity - Delphi"].split(","):
                available_geography = Geography.objects.get(name=available_geography, used_in="signal_sets")
                signal_set_obj.available_geographies.add(available_geography)
            signal_set_obj.save()
        except SignalSet.DoesNotExist as e:
            print(f"SignalSet.DoesNotExist: {e}")
