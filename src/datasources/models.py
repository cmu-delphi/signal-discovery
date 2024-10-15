from django.db import models
from django.utils.translation import gettext_lazy as _
from models_extensions.models import TimeStampedModel


class DataSource(TimeStampedModel):
    """
    Model to store data sources.
    """

    name: models.CharField = models.CharField(
        verbose_name=_('Name'),
        max_length=128,
        unique=True,
    )
    display_name: models.CharField = models.CharField(
        verbose_name=_('Display Name'),
        max_length=128,
        blank=True
    )
    description: models.TextField = models.TextField(
        verbose_name=_('Description'),
        blank=True,
    )
    license: models.CharField = models.CharField(
        verbose_name=_('License'),
        max_length=128,
        blank=True,
    )
    related_links: models.ManyToManyField = models.ManyToManyField(
        'base.Link',
        verbose_name=_('Related Links'),
        related_name='data_sources',
        blank=True,
    )

    class Meta:
        ordering: list[str] = ["name"]

    def __str__(self) -> str:
        """
        Returns the name of the data source as a string.

        :return: The name of the data source as a string.
        :rtype: str
        """
        return str(self.name)


class SourceSubdivision(TimeStampedModel):
    """
    Model to store source subdivisions.
    """

    name: models.CharField = models.CharField(
        verbose_name=_('Name'),
        max_length=128,
        unique=True,
    )
    display_name: models.CharField = models.CharField(
        verbose_name=_('Display Name'),
        max_length=128,
    )
    data_source: models.ForeignKey = models.ForeignKey(
        DataSource,
        verbose_name=_('Data Source'),
        related_name='source_subdivisions',
        on_delete=models.PROTECT,
    )

    class Meta:
        ordering: list[str] = ["name"]

    def __str__(self) -> str:
        """
        Returns the name of the source subdivision as a string.

        :return: The name of the source subdivision as a string.
        :rtype: str
        """
        return str(self.name)
