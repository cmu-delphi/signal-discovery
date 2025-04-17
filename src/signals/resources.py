from typing import Any

from import_export import resources
from import_export.results import RowResult
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget

from django.db.models import Max

from datasources.models import SourceSubdivision
from datasources.resources import process_links
from signal_sets.models import SignalSet
from signals.models import (
    Category,
    FormatType,
    GeographicScope,
    Geography,
    Pathogen,
    SeverityPyramidRung,
    Signal,
    SignalGeography,
    SignalType,
)


def fix_boolean_fields(row) -> Any:
    """
    Fixes boolean fields.
    """
    fields = [
        "Active",
        "Is Smoothed",
        "Is Weighted",
        "Is Cumulative",
        "Has StdErr",
        "Has Sample Size",
        "Include in indicator app",
    ]
    for k in fields:
        if row[k] == "TRUE":
            row[k] = True
        if row[k] == "FALSE" or row[k] == "":
            row[k] = False
    return row


def process_pathogen(row) -> None:
    """
    Processes pathogen.
    """
    if row["Pathogen/\nDisease Area"]:
        pathogens = row["Pathogen/\nDisease Area"].split(",")
        for pathogen in pathogens:
            pathogen = pathogen.strip()
            pathogen_obj, _ = Pathogen.objects.get_or_create(
                name=pathogen, used_in="signals", defaults={"used_in": "signals"}
            )


def process_signal_type(row) -> None:
    """
    Processes signal type.
    """
    if row["Indicator Type"]:
        signal_type = row["Indicator Type"]
        signal_type_obj, _ = SignalType.objects.get_or_create(name=signal_type)
        row["Indicator Type"] = signal_type_obj.id


def process_format_type(row) -> None:
    """
    Processes format type.
    """
    if row["Format"]:
        format_type = row["Format"].strip()
        format_type_obj, _ = FormatType.objects.get_or_create(name=format_type)
        row["Format"] = format_type_obj.id


def process_severity_pyramid_rungs(row) -> None:
    """
    Processes severity pyramid rungs.
    """
    if row["Surveillance Categories"]:
        severity_pyramid_rung = row["Surveillance Categories"].strip()
        if severity_pyramid_rung.startswith("None"):
            row["Surveillance Categories"] = None
        else:
            severity_pyramid_rung_obj, _ = SeverityPyramidRung.objects.get_or_create(
                name=severity_pyramid_rung,
                used_in="signals",
                defaults={"used_in": "signals", "display_name": severity_pyramid_rung},
            )
        row["Surveillance Categories"] = severity_pyramid_rung_obj.id
    else:
        none_severity_pyramid_rung_obj, _ = SeverityPyramidRung.objects.get_or_create(
            name="N/A",
            used_in="signals",
            defaults={"used_in": "signals", "display_name": "N/A"},
        )
        row["Surveillance Categories"] = none_severity_pyramid_rung_obj.id


def process_category(row) -> None:
    """
    Processes category.
    """
    if row["Category"]:
        category = row["Category"].strip()
        category_obj, _ = Category.objects.get_or_create(name=category)
        row["Category"] = category_obj.id


def process_geographic_scope(row) -> None:
    """
    Processes geographic scope.
    """
    if row["Geographic Coverage"]:
        geographic_scope = row["Geographic Coverage"]
        geographic_scope_obj, _ = GeographicScope.objects.get_or_create(
            name=geographic_scope, used_in="signals", defaults={"used_in": "signals"}
        )
        row["Geographic Coverage"] = geographic_scope_obj.id


def process_source(row) -> None:
    """
    Processes source.
    """
    if row["Source Subdivision"]:
        source = row["Source Subdivision"]
        source_obj, _ = SourceSubdivision.objects.get_or_create(name=source)
        row["Source Subdivision"] = source_obj.id


def process_available_geographies(row) -> None:
    """
    Processes available geographies.
    """
    if row["Geographic Levels"]:
        geographies: str = row["Geographic Levels"].split(",")
        delphi_aggregated_geographies: str = row["Delphi-Aggregated Geography"].split(
            ","
        )
        for geography in geographies:
            max_display_order_number = Geography.objects.filter(
                used_in="signals"
            ).aggregate(Max("display_order_number"))["display_order_number__max"]
            geography_instance, _ = Geography.objects.get_or_create(
                name=geography.strip(),
                used_in="signals",
                defaults={
                    "used_in": "signals",
                    "display_order_number": max_display_order_number + 1,
                },
            )
            try:
                signal = Signal.objects.get(
                    name=row["Indicator"], source=row["Source Subdivision"]
                )
            except KeyError:
                signal = Signal.objects.get(
                    name=row["Signal"], source=row["Source Subdivision"]
                )
            signal_geography, _ = SignalGeography.objects.get_or_create(
                geography=geography_instance, signal=signal
            )
            if geography in delphi_aggregated_geographies:
                signal_geography.aggregated_by_delphi = True
                signal_geography.save()


def process_base(row) -> None:
    if row["Signal BaseName"]:
        source: SourceSubdivision = SourceSubdivision.objects.get(
            name=row["Source Subdivision"]
        )
        base_signal: Signal = Signal.objects.get(
            name=row["Signal BaseName"], source=source
        )
        row["base"] = base_signal.id


class ModelResource(resources.ModelResource):
    def get_field_names(self):
        names = []
        for field in list(self.fields.values()):
            names.append(self.get_field_name(field))
        return names

    def import_row(self, row, instance_loader, **kwargs):
        # overriding import_row to ignore errors and skip rows that fail to import
        # without failing the entire import
        import_result = super(ModelResource, self).import_row(
            row, instance_loader, **kwargs
        )

        if import_result.import_type in [
            RowResult.IMPORT_TYPE_ERROR,
            RowResult.IMPORT_TYPE_INVALID,
        ]:
            import_result.diff = [row.get(name, "") for name in self.get_field_names()]

            # Add a column with the error message
            import_result.diff.append(
                "Errors: {}".format([err.error for err in import_result.errors])
            )
            # clear errors and mark the record to skip
            import_result.errors = []
            import_result.import_type = RowResult.IMPORT_TYPE_SKIP

        return import_result


class SignalBaseResource(ModelResource):
    """
    Resource class for importing Signals base.
    """

    name = Field(attribute="name", column_name="Signal")
    display_name = Field(attribute="display_name", column_name="Name")
    base = Field(
        attribute="base",
        column_name="base",
        widget=ForeignKeyWidget(Signal, field="id"),
    )
    source = Field(
        attribute="source",
        column_name="Source Subdivision",
        widget=ForeignKeyWidget(SourceSubdivision),
    )

    class Meta:
        model = Signal
        fields: list[str] = ["base", "name", "source", "display_name"]
        import_id_fields: list[str] = ["name", "source"]

    def before_import_row(self, row, **kwargs) -> None:
        """Post-processes each row after importing."""
        process_base(row)


class SignalResource(ModelResource):
    """
    Resource class for importing and exporting Signal models
    """

    name = Field(attribute="name", column_name="Signal")
    display_name = Field(attribute="display_name", column_name="Name")
    member_name = Field(attribute="member_name", column_name="Member API Name")
    member_short_name = Field(
        attribute="member_short_name", column_name="Member Short Name"
    )
    member_description = Field(
        attribute="member_description", column_name="Member Description"
    )
    pathogen = Field(
        attribute="pathogen",
        column_name="Pathogen/\nDisease Area",
        widget=ManyToManyWidget(Pathogen, field="name", separator=","),
    )
    signal_type = Field(
        attribute="signal_type",
        column_name="Indicator Type",
        widget=ForeignKeyWidget(SignalType),
    )
    active = Field(attribute="active", column_name="Active")
    description = Field(attribute="description", column_name="Description")
    short_description = Field(
        attribute="short_description", column_name="Short Description"
    )
    format_type = Field(
        attribute="format_type",
        column_name="Format",
        widget=ForeignKeyWidget(FormatType),
    )
    time_type = Field(attribute="time_type", column_name="Time Type")
    time_label = Field(attribute="time_label", column_name="Time Label")
    reporting_cadence = Field(
        attribute="reporting_cadence", column_name="Reporting Cadence"
    )
    typical_reporting_lag = Field(
        attribute="typical_reporting_lag", column_name="Typical Reporting Lag"
    )
    typical_revision_cadence = Field(
        attribute="typical_revision_cadence", column_name="Typical Revision Cadence"
    )
    demographic_scope = Field(
        attribute="demographic_scope", column_name="Population"
    )
    severity_pyramid_rung = Field(
        attribute="severity_pyramid_rung",
        column_name="Surveillance Categories",
        widget=ForeignKeyWidget(SeverityPyramidRung),
    )
    category = Field(
        attribute="category",
        column_name="Category",
        widget=ForeignKeyWidget(Category),
    )
    geographic_scope = Field(
        attribute="geographic_scope",
        column_name="Geographic Coverage",
        widget=ForeignKeyWidget(GeographicScope),
    )
    available_geographies = Field(
        attribute="available_geography",
        column_name="Geographic Levels",
        widget=ManyToManyWidget(Geography, field="name", separator=","),
    )
    temporal_scope_start = Field(
        attribute="temporal_scope_start", column_name="Temporal Scope Start"
    )
    temporal_scope_start_note = Field(
        attribute="temporal_scope_start_note", column_name="Temporal Scope Start Note"
    )
    temporal_scope_end = Field(
        attribute="temporal_scope_end", column_name="Temporal Scope End"
    )
    temporal_scope_end_note = Field(
        attribute="temporal_scope_end_note", column_name="Temporal Scope End Note"
    )
    is_smoothed = Field(attribute="is_smoothed", column_name="Is Smoothed")
    is_weighted = Field(attribute="is_weighted", column_name="Is Weighted")
    is_cumulative = Field(attribute="is_cumulative", column_name="Is Cumulative")
    has_stderr = Field(attribute="has_stderr", column_name="Has StdErr")
    has_sample_size = Field(attribute="has_sample_size", column_name="Has Sample Size")
    high_values_are = Field(attribute="high_values_are", column_name="High Values Are")
    source = Field(
        attribute="source",
        column_name="Source Subdivision",
        widget=ForeignKeyWidget(SourceSubdivision),
    )
    data_censoring = Field(attribute="data_censoring", column_name="Data Censoring")
    missingness = Field(attribute="missingness", column_name="Missingness")
    organization_access_list = Field(
        attribute="organization_access_list", column_name="Who may access this indicator?"
    )
    organization_sharing_list = Field(
        attribute="organization_sharing_list",
        column_name="Who may be told about this indicator?",
    )
    license = Field(attribute="license", column_name="Data Use Terms")
    restrictions = Field(attribute="restrictions", column_name="Use Restrictions")
    signal_set = Field(
        attribute="signal_set",
        column_name="Indicator Set",
        widget=ForeignKeyWidget(SignalSet, field="name"),
    )

    class Meta:
        model = Signal
        fields: list[str] = [
            "name",
            "display_name",
            "member_name",
            "member_short_name",
            "member_description",
            "pathogen",
            "signal_type",
            "active",
            "description",
            "short_description",
            "time_label",
            "reporting_cadence",
            "typical_reporting_lag",
            "typical_revision_cadence",
            "demographic_scope",
            "category",
            "geographic_scope",
            "available_geographies",
            "temporal_scope_start",
            "temporal_scope_start_note",
            "temporal_scope_end",
            "temporal_scope_end_note",
            "is_smoothed",
            "is_weighted",
            "is_cumulative",
            "has_stderr",
            "has_sample_size",
            "high_values_are",
            "source",
            "data_censoring",
            "missingness",
            "organization_access_list",
            "organization_sharing_list",
            "license",
            "restrictions",
            "time_type",
            "signal_set",
            "format_type",
            "severity_pyramid_rung",
        ]
        import_id_fields: list[str] = ["name", "source"]
        store_instance = True
        skip_unchanged = True

    def before_import_row(self, row, **kwargs) -> None:
        fix_boolean_fields(row)
        process_pathogen(row)
        process_signal_type(row)
        process_format_type(row)
        process_severity_pyramid_rungs(row)
        process_category(row)
        process_geographic_scope(row)
        process_source(row)
        process_links(row, dua_column_name="Link to DUA", link_column_name="Link")
        if not row.get("Indicator Set"):
            row["Indicator Set"] = None
        if not row.get("Source Subdivision"):
            row["Source Subdivision"] = None

    def skip_row(self, instance, original, row, import_validation_errors=None):
        if not row["Include in indicator app"]:
            try:
                signal = Signal.objects.get(
                    name=row["Signal"], source=row["Source Subdivision"]
                )
                signal.delete()
            except Signal.DoesNotExist:
                pass
            return True

    def after_import_row(self, row, row_result, **kwargs):
        try:
            signal_obj = Signal.objects.get(id=row_result.object_id)
            for link in row["Links"]:
                signal_obj.related_links.add(link)
            process_available_geographies(row)
            signal_obj.severity_pyramid_rung = SeverityPyramidRung.objects.get(id=row["Surveillance Categories"])
            signal_obj.format_type = FormatType.objects.get(id=row["Format"])
            signal_obj.save()
        except Signal.DoesNotExist as e:
            print(f"Signal.DoesNotExist: {e}")


class OtherEndpointSignalResource(ModelResource):
    """
    Resource class for importing and exporting Signal models
    """

    name = Field(attribute="name", column_name="Indicator")
    display_name = Field(attribute="display_name", column_name="Name")
    member_name = Field(attribute="member_name", column_name="Member API Name")
    member_short_name = Field(
        attribute="member_short_name", column_name="Member Short Name"
    )
    member_description = Field(
        attribute="member_description", column_name="Member Description"
    )
    pathogen = Field(
        attribute="pathogen",
        column_name="Pathogen/\nDisease Area",
        widget=ManyToManyWidget(Pathogen, field="name", separator=","),
    )
    signal_type = Field(
        attribute="signal_type",
        column_name="Indicator Type",
        widget=ForeignKeyWidget(SignalType),
    )
    active = Field(attribute="active", column_name="Active")
    description = Field(attribute="description", column_name="Description")
    short_description = Field(
        attribute="short_description", column_name="Short Description"
    )
    format_type = Field(
        attribute="format_type",
        column_name="Format",
        widget=ForeignKeyWidget(FormatType),
    )
    time_type = Field(attribute="time_type", column_name="Time Type")
    time_label = Field(attribute="time_label", column_name="Time Label")
    reporting_cadence = Field(
        attribute="reporting_cadence", column_name="Reporting Cadence"
    )
    typical_reporting_lag = Field(
        attribute="typical_reporting_lag", column_name="Typical Reporting Lag"
    )
    typical_revision_cadence = Field(
        attribute="typical_revision_cadence", column_name="Typical Revision Cadence"
    )
    demographic_scope = Field(
        attribute="demographic_scope", column_name="Population"
    )
    severity_pyramid_rung = Field(
        attribute="severity_pyramid_rung",
        column_name="Surveillance Categories",
        widget=ForeignKeyWidget(SeverityPyramidRung),
    )
    category = Field(
        attribute="category",
        column_name="Category",
        widget=ForeignKeyWidget(Category),
    )
    geographic_scope = Field(
        attribute="geographic_scope",
        column_name="Geographic Coverage",
        widget=ForeignKeyWidget(GeographicScope),
    )
    available_geographies = Field(
        attribute="available_geography",
        column_name="Geographic Levels",
        widget=ManyToManyWidget(Geography, field="name", separator=","),
    )
    temporal_scope_start = Field(
        attribute="temporal_scope_start", column_name="Temporal Scope Start"
    )
    temporal_scope_start_note = Field(
        attribute="temporal_scope_start_note", column_name="Temporal Scope Start Note"
    )
    temporal_scope_end = Field(
        attribute="temporal_scope_end", column_name="Temporal Scope End"
    )
    temporal_scope_end_note = Field(
        attribute="temporal_scope_end_note", column_name="Temporal Scope End Note"
    )
    is_smoothed = Field(attribute="is_smoothed", column_name="Is Smoothed")
    is_weighted = Field(attribute="is_weighted", column_name="Is Weighted")
    is_cumulative = Field(attribute="is_cumulative", column_name="Is Cumulative")
    has_stderr = Field(attribute="has_stderr", column_name="Has StdErr")
    has_sample_size = Field(attribute="has_sample_size", column_name="Has Sample Size")
    high_values_are = Field(attribute="high_values_are", column_name="High Values Are")
    source = Field(
        attribute="source",
        column_name="Source Subdivision",
        widget=ForeignKeyWidget(SourceSubdivision),
    )
    data_censoring = Field(attribute="data_censoring", column_name="Data Censoring")
    missingness = Field(attribute="missingness", column_name="Missingness")
    organization_access_list = Field(
        attribute="organization_access_list", column_name="Who may access this indicator?"
    )
    organization_sharing_list = Field(
        attribute="organization_sharing_list",
        column_name="Who may be told about this indicator?",
    )
    license = Field(attribute="license", column_name="Data Use Terms")
    restrictions = Field(attribute="restrictions", column_name="Use Restrictions")
    signal_set = Field(
        attribute="signal_set",
        column_name="Indicator Set",
        widget=ForeignKeyWidget(SignalSet, field="name"),
    )

    class Meta:
        model = Signal
        fields: list[str] = [
            "name",
            "display_name",
            "member_name",
            "member_short_name",
            "member_description",
            "pathogen",
            "signal_type",
            "active",
            "description",
            "short_description",
            "time_label",
            "reporting_cadence",
            "typical_reporting_lag",
            "typical_revision_cadence",
            "demographic_scope",
            "category",
            "geographic_scope",
            "available_geographies",
            "temporal_scope_start",
            "temporal_scope_start_note",
            "temporal_scope_end",
            "temporal_scope_end_note",
            "is_smoothed",
            "is_weighted",
            "is_cumulative",
            "has_stderr",
            "has_sample_size",
            "high_values_are",
            "source",
            "data_censoring",
            "missingness",
            "organization_access_list",
            "organization_sharing_list",
            "license",
            "restrictions",
            "time_type",
            "signal_set",
            "format_type",
            "severity_pyramid_rung",
        ]
        import_id_fields: list[str] = ["name", "source"]
        store_instance = True
        skip_unchanged = True

    def before_import_row(self, row, **kwargs) -> None:
        fix_boolean_fields(row)
        process_pathogen(row)
        process_signal_type(row)
        process_format_type(row)
        process_severity_pyramid_rungs(row)
        process_category(row)
        process_geographic_scope(row)
        process_source(row)
        process_links(row, dua_column_name="Link to DUA", link_column_name="Link")
        if not row.get("Indicator Set"):
            row["Indicator Set"] = None
        if not row.get("Source Subdivision"):
            row["Source Subdivision"] = None

    def skip_row(self, instance, original, row, import_validation_errors=None):
        if not row["Include in indicator app"]:
            try:
                signal = Signal.objects.get(
                    name=row["Indicator"], source=row["Source Subdivision"]
                )
                signal.delete()
            except Signal.DoesNotExist:
                pass
            return True

    def after_import_row(self, row, row_result, **kwargs):
        try:
            signal_obj = Signal.objects.get(id=row_result.object_id)
            for link in row["Links"]:
                signal_obj.related_links.add(link)
            process_available_geographies(row)
            signal_obj.severity_pyramid_rung = SeverityPyramidRung.objects.get(id=row["Surveillance Categories"])
            signal_obj.format_type = FormatType.objects.get(id=row["Format"])
            signal_obj.save()
        except Signal.DoesNotExist as e:
            print(f"Signal.DoesNotExist: {e}")
