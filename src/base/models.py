from django.db import models
from django.utils.translation import gettext_lazy as _
from models_extensions.models import TimeStampedModel


class Link(TimeStampedModel):
    """
    A model representing a Link.
    """
    link_type: models.CharField = models.CharField(
        help_text=_('Link type'),
        max_length=128
    )
    url = models.URLField(
        help_text=_('Link URL'),
        max_length=255,
        unique=True
    )

    class Meta:
        verbose_name_plural: str = "links"

    def __str__(self) -> str:
        """
        Returns the name of the link as a string.

        :return: The name of link as a string.
        :rtype: str
        """
        return str(self.url)