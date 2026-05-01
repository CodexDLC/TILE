from django.db import models
from django.utils.translation import gettext_lazy as _
from system.models.mixins import OrderableMixin, TimestampMixin


class TabsBlock(TimestampMixin):
    heading = models.CharField(max_length=255, blank=True)
    intro = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.heading or "Tabs"

    class Meta:
        verbose_name = _("Блок: вкладки")
        verbose_name_plural = _("Блоки: вкладки")


class TabItem(OrderableMixin):
    block = models.ForeignKey(TabsBlock, on_delete=models.CASCADE, related_name="items")
    label = models.CharField(max_length=128)
    heading = models.CharField(max_length=255, blank=True)
    body = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.label

    class Meta(OrderableMixin.Meta):
        verbose_name = _("Вкладка")
        verbose_name_plural = _("Вкладки")
