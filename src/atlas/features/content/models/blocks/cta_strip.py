from django.db import models
from django.utils.translation import gettext_lazy as _
from system.models.mixins import TimestampMixin


class CtaStripBlock(TimestampMixin):
    eyebrow = models.CharField(max_length=128, blank=True)
    title = models.CharField(max_length=255)
    text = models.TextField(blank=True)
    cta_label = models.CharField(max_length=128, blank=True)
    cta_url = models.CharField(max_length=255, blank=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = _("Блок: CTA")
        verbose_name_plural = _("Блоки: CTA")
