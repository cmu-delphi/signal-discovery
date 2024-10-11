from django.db import models
from django.utils.translation import gettext_lazy as _


class SignalSetGeography(models.Model):
    geography = models.ForeignKey(
        "signals.Geography",
        on_delete=models.CASCADE,
        related_name="geography_signal_sets",
    )
    signal_set = models.ForeignKey(
        "signal_sets.SignalSet",
        on_delete=models.CASCADE,
        related_name="geography_signal_sets",
    )
    aggregated_by_delphi = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Signal Geographies"
        unique_together = ("geography", "signal_set")

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


class SignalSet(models.Model):
    name: models.CharField = models.CharField(
        verbose_name="name",
        max_length=255,
        unique=True,
    )

    data_description: models.TextField = models.TextField(
        verbose_name="Data Description",
        blank=True,
    )

    maintainer_name: models.CharField = models.CharField(
        verbose_name="Maintainer Name",
        max_length=255,
        blank=True,
    )

    maintainer_email: models.CharField = models.CharField(
        verbose_name="Maintainer Email",
        max_length=255,
        blank=True,
    )

    organization: models.CharField = models.CharField(
        verbose_name="Organization",
        max_length=255,
        blank=True,
    )

    data_source: models.CharField = models.CharField(
        verbose_name="Data Source",
        max_length=255,
        blank=True,
    )

    language: models.CharField = models.CharField(
        verbose_name="Language",
        max_length=255,
        blank=True,
    )

    version_number: models.CharField = models.CharField(
        verbose_name="Version Number",
        max_length=255,
        blank=True,
    )

    origin_datasource: models.TextField = models.TextField(
        verbose_name="Origin Data Source",
        blank=True,
    )

    pathogens: models.ManyToManyField = models.ManyToManyField(
        "signals.Pathogen",
        related_name="signal_sets",
        verbose_name="Pathogen",
        help_text="Pathogen(s) associated with the signal set.",
        blank=True,
    )

    data_type: models.CharField = models.CharField(
        verbose_name="Data Type",
        max_length=255,
        blank=True,
    )

    geographic_scope: models.ForeignKey = models.ForeignKey(
        "signals.GeographicScope",
        related_name="signal_sets",
        verbose_name="Geographic Scope",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    available_geographies: models.ManyToManyField = models.ManyToManyField(
        "signals.Geography",
        related_name="signal_sets",
        verbose_name="Available Geography",
        through="signal_sets.SignalSetGeography",
        blank=True,
    )

    geographic_granulalarity: models.CharField = models.CharField(
        verbose_name="Geographic Granularity",
        max_length=255,
        blank=True,
    )

    preprocessing_description: models.CharField = models.CharField(
        verbose_name="Preprocessing Description",
        max_length=255,
        blank=True,
    )

    temporal_scope_start: models.CharField = models.CharField(
        max_length=255,
        verbose_name=_("temporal scope start"),
        help_text=_("Temporal scope start of the signal set."),
    )

    temporal_scope_end: models.CharField = models.CharField(
        max_length=255,
        verbose_name=_("temporal scope end"),
        help_text=_("Temporal scope end of the signal set."),
    )

    temporal_granularity: models.CharField = models.CharField(
        max_length=255,
        verbose_name=_("temporal granularity"),
        help_text=_("Temporal granularity of the signal set."),
    )

    reporting_cadence: models.CharField = models.CharField(
        max_length=255,
        verbose_name=_("reporting cadence"),
        help_text=_("Reporting cadence of the signal set."),
    )

    reporting_lag: models.CharField = models.CharField(
        max_length=255,
        verbose_name=_("typical reporting lag"),
        help_text=_("Typical reporting lag of the signal set."),
    )

    revision_cadence: models.CharField = models.CharField(
        max_length=255,
        verbose_name=_("revision cadence"),
        help_text=_("Revision cadence of the signal set."),
    )

    demographic_scope: models.CharField = models.CharField(
        max_length=255,
        verbose_name=_("demographic scope"),
        help_text=_("Demographic scope of the signal set."),
    )

    demographic_granularity: models.CharField = models.CharField(
        max_length=255,
        verbose_name=_("demographic granularity"),
        help_text=_("Demographic granularity of the signal set."),
    )

    severity_pyramid_rungs: models.ManyToManyField = models.ManyToManyField(
        "signals.SeverityPyramidRung",
        related_name="signal_sets",
        help_text=_("Severity pyramid rungs of the signal set."),
        blank=True,
    )

    censoring: models.CharField = models.CharField(
        max_length=255,
        verbose_name=_("data censoring"),
        help_text=_("Data censoring of the signal set."),
        null=True,
        blank=True,
    )

    missingness: models.TextField = models.TextField(
        verbose_name=_("missingness"),
        help_text=_("Missingness of the signal set."),
        blank=True
    )

    dua_required: models.CharField = models.CharField(
        verbose_name=_("DUA Required"),
        max_length=128,
        help_text=_(
            "Whether a data use agreement is required to access the signal set."
        ),
    )

    license: models.CharField = models.CharField(
        max_length=255,
        verbose_name=_("license"),
        help_text=_("License of the signal set."),
    )

    dataset_location: models.CharField = models.CharField(
        max_length=255,
        verbose_name=_("dataset location"),
        help_text=_("Location of the dataset."),
    )

    link_to_dictionary: models.CharField = models.CharField(
        max_length=255,
        verbose_name=_("link to dictionary"),
        help_text=_("Link to the dictionary."),
    )

    class Meta:
        unique_together = ("name", "data_source")
        ordering = ["name"]
