from django.db import models
from django.utils.translation import gettext_lazy as _
from system.models.mixins import TimestampMixin


class RichTextBlock(TimestampMixin):
    heading = models.CharField(max_length=255, blank=True)
    body = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.heading or "Rich text"

    class Meta:
        verbose_name = _("Блок: текст")
        verbose_name_plural = _("Блоки: текст")
