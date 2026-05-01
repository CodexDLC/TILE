from django.db import models
from django.utils.translation import gettext_lazy as _
from system.models.mixins import TimestampMixin


class PullQuoteBlock(TimestampMixin):
    quote = models.TextField()
    attribution = models.CharField(max_length=255, blank=True)

    def __str__(self) -> str:
        return self.quote[:80]

    class Meta:
        verbose_name = _("Блок: цитата")
        verbose_name_plural = _("Блоки: цитаты")
