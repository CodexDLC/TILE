from django.db import models
from django.utils.translation import gettext_lazy as _
from system.models.mixins import OrderableMixin, TimestampMixin


class FactsListBlock(TimestampMixin):
    heading = models.CharField(max_length=255, blank=True)
    intro = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.heading or "Facts list"

    class Meta:
        verbose_name = _("Блок: факты")
        verbose_name_plural = _("Блоки: факты")


class FactItem(OrderableMixin):
    block = models.ForeignKey(FactsListBlock, on_delete=models.CASCADE, related_name="items")
    label = models.CharField(max_length=128)
    value = models.CharField(max_length=255)
    note = models.CharField(max_length=255, blank=True)

    def __str__(self) -> str:
        return self.label

    class Meta(OrderableMixin.Meta):
        verbose_name = _("Факт")
        verbose_name_plural = _("Факты")
