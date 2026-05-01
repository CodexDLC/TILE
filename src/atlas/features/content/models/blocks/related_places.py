from django.db import models
from django.utils.translation import gettext_lazy as _
from system.models.mixins import TimestampMixin


class RelatedPlacesBlock(TimestampMixin):
    heading = models.CharField(max_length=255, blank=True)
    intro = models.TextField(blank=True)
    places = models.ManyToManyField("places.Place", blank=True, related_name="related_blocks")

    def __str__(self) -> str:
        return self.heading or "Related places"

    class Meta:
        verbose_name = _("Блок: связанные места")
        verbose_name_plural = _("Блоки: связанные места")
