from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from models_extensions.models import TimeStampedModel

USED_IN_CHOICES = (
    ("signals", "Signals"),
    ("signal_sets", "Signal Sets"),
)


class Pathogen(TimeStampedModel):
    """Model for representing pathogens."""

    name: models.CharField = models.CharField(
        max_length=128,
        verbose_name=_("name"),
        help_text=_("Name of the pathogen."),
    )

    display_name: models.CharField = models.CharField(
        max_length=128, null=True, blank=True
    )

    used_in: models.CharField = models.CharField(
        max_length=11,
        choices=USED_IN_CHOICES,
        default="signals",
    )

    class Meta:
        verbose_name_plural: str = "Pathogens"
        unique_together: list[str] = ["name", "used_in"]

    def __str__(self) -> str:
        """Returns the name of the signal type as a string."""
        return str(self.display_name) if self.display_name else str(self.name)


class SignalType(TimeStampedModel):
    """Model for representing signal types."""

    name: models.CharField = models.CharField(
        max_length=128,
        unique=True,
        verbose_name=_("name"),
        help_text=_("Name of the signal type."),
    )
    display_name: models.CharField = models.CharField(
        max_length=128,
        verbose_name=_("display name"),
        help_text=_("Display name of the signal type."),
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        """Returns the name of the signal type as a string."""
        return str(self.display_name) if self.display_name else str(self.name)


class SeverityPyramidRung(TimeStampedModel):
    """Model for representing severity pyramid rungs."""

    name: models.CharField = models.CharField(
        max_length=255,
        verbose_name=_("name"),
        help_text=_("Name of the severity pyramid rung."),
    )
    display_name: models.CharField = models.CharField(
        max_length=255,
        verbose_name=_("display name"),
        help_text=_("Display name of the severity pyramid rung."),
        null=True,
        blank=True,
    )

    used_in: models.CharField = models.CharField(
        max_length=11,
        choices=USED_IN_CHOICES,
        default="signals",
    )

    display_order_number: models.IntegerField = models.IntegerField(
        verbose_name=_("display order number"),
        help_text=_("Display order number of the severity pyramid rung."),
        null=True,
    )

    class Meta:
        verbose_name_plural: str = "Severity Pyramid Rungs"
        unique_together: list[str] = ["name", "used_in"]

    def __str__(self) -> str:
        return str(self.display_name) if self.display_name else str(self.name)


class FormatType(TimeStampedModel):
    """Model for representing format types."""

    name: models.CharField = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_("name"),
        help_text=_("Name of the format type."),
    )
    display_name: models.CharField = models.CharField(
        max_length=255,
        verbose_name=_("display name"),
        help_text=_("Display name of the format type."),
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name_plural: str = "Format Types"

    def __str__(self) -> str:
        return str(self.display_name) if self.display_name else str(self.name)


class Category(TimeStampedModel):
    """Model for representing categories."""

    name: models.CharField = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_("name"),
        help_text=_("Name of the category."),
    )
    display_name: models.CharField = models.CharField(
        max_length=255,
        verbose_name=_("display name"),
        help_text=_("Display name of the category."),
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return str(self.display_name) if self.display_name else str(self.name)


class GeographicScope(TimeStampedModel):
    """Model for representing geographic scopes."""

    name: models.CharField = models.CharField(
        max_length=255,
        verbose_name=_("name"),
        help_text=_("Name of the geographic scope."),
    )

    used_in: models.CharField = models.CharField(
        max_length=11,
        choices=USED_IN_CHOICES,
        default="signals",
    )

    class Meta:
        verbose_name_plural: str = "Geographic Scopes"
        unique_together: list[str] = ["name", "used_in"]

    def __str__(self) -> str:
        return str(self.name)


class Geography(TimeStampedModel):
    """Model for representing geographies."""

    name: models.CharField = models.CharField(
        max_length=255,
        verbose_name=_("name"),
        help_text=_("Name of the geography."),
    )

    display_name: models.CharField = models.CharField(
        max_length=255,
        verbose_name=_("display name"),
        help_text=_("Display name of the geography."),
    )

    display_order_number: models.IntegerField = models.IntegerField(
        verbose_name=_("display order number"),
        help_text=_("Display order number of the geography."),
    )

    used_in: models.CharField = models.CharField(
        max_length=11,
        choices=USED_IN_CHOICES,
        default="signals",
    )

    class Meta:
        verbose_name_plural: str = "geographies"
        ordering: list[str] = ["display_order_number"]
        unique_together: list[str] = ["name", "used_in"]

    def __str__(self) -> str:
        """
        Returns the name of the available geography as a string.

        :return: The name of the available geography as a string.
        :rtype: str
        """
        return str(self.display_name) if self.display_name else str(self.name)


class SignalGeography(models.Model):
    geography = models.ForeignKey(
        "signals.Geography", on_delete=models.CASCADE, related_name="geography_signals"
    )
    signal = models.ForeignKey(
        "signals.Signal", on_delete=models.CASCADE, related_name="geography_signals"
    )
    aggregated_by_delphi = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Signal Geographies"
        unique_together = ("geography", "signal")

    @property
    def display_name(self) -> str:
        """
        Returns the display name of the geography signal.
        """
        return (
            f"{self.geography.name} (by Delphi)"
            if self.aggregated_by_delphi
            else self.geography.name
        )


class GeographyUnit(TimeStampedModel):
    """
    A model representing a geography (geo-level) unit.
    """

    geo_id: models.CharField = models.CharField(help_text=_("Geo ID"), max_length=128)
    name: models.CharField = models.CharField(help_text=_("Name"), max_length=128)
    display_name: models.CharField = models.CharField(
        help_text=_("Display Name"), max_length=128
    )
    level: models.IntegerField = models.IntegerField(help_text=_("Level"))

    geography: models.ForeignKey = models.ForeignKey(
        "signals.Geography",
        related_name="geography_units",
        help_text=_("Geography"),
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        """
        Returns the name of the geography unit as a string.

        :return: The name of the geography unit as a string.
        :rtype: str
        """
        return str(self.name)


class Signal(TimeStampedModel):
    """Model for representing signals."""

    name: models.CharField = models.CharField(
        max_length=255,
        verbose_name=_("name"),
        help_text=_("Name of the signal."),
    )
    display_name: models.CharField = models.CharField(
        max_length=255,
        verbose_name=_("display name"),
        help_text=_("Display name of the signal."),
        null=True,
        blank=True,
    )
    member_name: models.CharField = models.CharField(
        max_length=255,
        verbose_name=_("member name"),
        help_text=_("Member name of the signal."),
        null=True,
        blank=True,
    )
    member_short_name: models.CharField = models.CharField(
        max_length=255,
        verbose_name=_("member short name"),
        help_text=_("Member short name of the signal."),
        null=True,
        blank=True,
    )
    member_description: models.TextField = models.TextField(
        verbose_name=_("member description"),
        help_text=_("Member description of the signal."),
        null=True,
        blank=True,
    )
    pathogen: models.ManyToManyField = models.ManyToManyField(
        "signals.Pathogen",
        related_name="signals",
        help_text=_("Pathogen/Disease area"),
        blank=True,
    )
    signal_type: models.ForeignKey = models.ForeignKey(
        "signals.SignalType",
        related_name="signals",
        help_text=_("Type of the signal."),
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    active: models.BooleanField = models.BooleanField(
        default=False,
        verbose_name=_("active"),
        help_text=_("Ongoing"),
        null=True,
        blank=True,
    )
    description: models.TextField = models.TextField(
        verbose_name=_("description"),
        help_text=_("Description of the signal."),
        null=True,
        blank=True,
    )
    short_description: models.TextField = models.TextField(
        verbose_name=_("short description"),
        help_text=_("Short description of the signal."),
        null=True,
        blank=True,
    )
    format_type: models.ForeignKey = models.ForeignKey(
        "signals.FormatType",
        related_name="signals",
        help_text=_("Format type of the signal."),
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    time_type: models.CharField = models.CharField(
        max_length=255,
        verbose_name=_("time type"),
        help_text=_("Time type of the signal."),
        null=True,
        blank=True,
    )
    time_label: models.CharField = models.CharField(
        max_length=255,
        verbose_name=_("time label"),
        help_text=_("Time label of the signal."),
        null=True,
        blank=True,
    )
    reporting_cadence: models.CharField = models.CharField(
        max_length=255,
        verbose_name=_("reporting cadence"),
        help_text=_("Reporting cadence of the signal."),
        null=True,
        blank=True,
    )
    typical_reporting_lag: models.CharField = models.CharField(
        max_length=255,
        verbose_name=_("typical reporting lag"),
        help_text=_("Typical reporting lag of the signal."),
        null=True,
        blank=True,
    )
    typical_revision_cadence: models.TextField = models.TextField(
        verbose_name=_("typical revision cadence"),
        help_text=_("Typical revision cadence of the signal."),
        null=True,
        blank=True,
    )
    demographic_scope: models.CharField = models.CharField(
        max_length=255,
        verbose_name=_("demographic scope"),
        help_text=_("Demographic scope of the signal."),
        null=True,
        blank=True,
    )
    severity_pyramid_rung: models.ForeignKey = models.ForeignKey(
        "signals.SeverityPyramidRung",
        related_name="signals",
        help_text=_("Severity pyramid rungs of the signal."),
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    category: models.ForeignKey = models.ForeignKey(
        "signals.Category",
        related_name="signals",
        help_text=_("Category of the signal."),
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    related_links: models.ManyToManyField = models.ManyToManyField(
        "base.Link",
        related_name="signals",
        help_text=_("Related signal links."),
        blank=True,
    )
    geographic_scope: models.ForeignKey = models.ForeignKey(
        "signals.GeographicScope",
        related_name="signals",
        help_text=_("Geographic scope of the signal."),
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    available_geography: models.ManyToManyField = models.ManyToManyField(
        "signals.Geography",
        related_name="signals",
        help_text=_("Available geographies for the signal."),
        through="signals.SignalGeography",
        blank=True,
    )
    temporal_scope_start: models.CharField = models.CharField(
        max_length=255,
        verbose_name=_("temporal scope start"),
        help_text=_("Temporal scope start of the signal."),
        null=True,
        blank=True,
    )
    temporal_scope_start_note: models.TextField = models.TextField(
        verbose_name=_("temporal scope start note"),
        help_text=_("Temporal scope start note of the signal."),
        null=True,
        blank=True,
    )
    temporal_scope_end: models.CharField = models.CharField(
        max_length=255,
        verbose_name=_("temporal scope end"),
        help_text=_("Temporal scope end of the signal."),
        null=True,
        blank=True,
    )
    temporal_scope_end_note: models.TextField = models.TextField(
        verbose_name=_("temporal scope end note"),
        help_text=_("Temporal scope end note of the signal."),
        null=True,
        blank=True,
    )
    is_smoothed: models.BooleanField = models.BooleanField(
        default=False,
        verbose_name=_("is smoothed"),
        help_text=_("Is smoothed"),
        null=True,
        blank=True,
    )
    is_weighted: models.BooleanField = models.BooleanField(
        default=False,
        verbose_name=_("is weighted"),
        help_text=_("Is weighted"),
        null=True,
        blank=True,
    )
    is_cumulative: models.BooleanField = models.BooleanField(
        default=False,
        verbose_name=_("is cumulative"),
        help_text=_("Is cumulative"),
        null=True,
        blank=True,
    )
    has_stderr: models.BooleanField = models.BooleanField(
        default=False,
        verbose_name=_("has stderr"),
        help_text=_("Has stderr"),
        null=True,
        blank=True,
    )
    has_sample_size: models.BooleanField = models.BooleanField(
        default=False,
        verbose_name=_("has sample size"),
        help_text=_("Has sample size"),
        null=True,
        blank=True,
    )
    high_values_are: models.CharField = models.CharField(
        max_length=128, help_text=_("High values are"), null=True, blank=True
    )
    source: models.ForeignKey = models.ForeignKey(
        "datasources.SourceSubdivision",
        related_name="signals",
        help_text=_("Source Subdivision"),
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    data_censoring: models.TextField = models.TextField(
        help_text=_("Data censoring"), null=True, blank=True
    )
    missingness: models.TextField = models.TextField(
        help_text=_("Missingness"), null=True, blank=True
    )
    organization_access_list: models.CharField = models.CharField(
        max_length=128,
        help_text=_("Organisations Access List. Who may access this signal?"),
        null=True,
        blank=True,
    )
    organization_sharing_list: models.CharField = models.CharField(
        max_length=128,
        help_text=_("Organisations Sharing List. Who may share this signal?"),
        null=True,
        blank=True,
    )
    license: models.CharField = models.CharField(max_length=128, help_text=_("License"))
    restrictions: models.TextField = models.TextField(
        help_text=_("Restrictions"), null=True, blank=True
    )
    last_updated: models.DateField = models.DateField(
        help_text=_("Last Updated"), null=True, blank=True
    )
    from_date: models.DateField = models.DateField(
        help_text=_("From Date"), null=True, blank=True
    )
    to_date: models.DateField = models.DateField(
        help_text=_("To Date"), null=True, blank=True
    )
    signal_availability_days: models.IntegerField = models.IntegerField(
        help_text=_("Signal Availability Days"), null=True, blank=True
    )

    base: models.ForeignKey = models.ForeignKey(
        "self",
        related_name="base_for",
        help_text=_("Base signal"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    signal_set: models.ForeignKey = models.ForeignKey(
        "signal_sets.SignalSet",
        related_name="signals",
        help_text=_("Signal Set"),
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    class Meta:
        unique_together = ["name", "source"]
        ordering: list[str] = ["modified"]

    @property
    def same_base_signals(self):
        """
        Returns the signals that have the same base signal.
        """
        return self.base.base_for.exclude(id=self.id) if self.base else None

    def __str__(self) -> str:
        """
        Returns the name of the signal as a string.

        """
        return str(self.name)

    def clean(self) -> None:
        """
        Validate that the signal has a base if any other signals exist.

        Raises:
            ValidationError: If there are other signals and this signal doesn't have a base.
        """
        if Signal.objects.exists() and not self.base:
            raise ValidationError(_("Signal should have base."))

    @property
    def get_display_name(self):
        if self.display_name:
            return self.display_name
        if self.member_name:
            return self.member_name
        else:
            return self.name


class OtherEndointSignal(Signal):
    class Meta:
        proxy = True
        verbose_name = "Other Endpoint Signal"
        verbose_name_plural = "Other Endpoint Signals"


class SignalsDbView(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    active = models.BooleanField()
    display_name = models.CharField(max_length=255)
    datasource = models.CharField(max_length=255)
    description = models.TextField()
    geographic_scope = models.CharField(max_length=255)
    temporal_scope_start = models.CharField(max_length=255)
    temporal_scope_end = models.CharField(max_length=255)
    time_type = models.CharField(max_length=255)
    reporting_cadence = models.CharField(max_length=255)
    typical_reporting_lag = models.CharField(max_length=255)
    typical_revision_cadence = models.TextField()
    demographic_scope = models.CharField(max_length=255)
    severity_pyramid_rung = models.CharField(max_length=255)
    missingness = models.TextField()
    license = models.CharField(max_length=255)
    restrictions = models.TextField()
    available_geography = models.CharField(max_length=255)
    pathogens = models.CharField(max_length=255)
    from_date = models.DateField()
    to_date = models.DateField()
    signal_availability_days = models.IntegerField()

    class Meta:
        managed = False
        db_table = "signals_signal_view"

    @property
    def get_available_geographies(self):
        return self.available_geography.split(",") if self.available_geography else []

    @property
    def get_pathogens(self):
        return self.pathogens.split(",") if self.pathogens else []

