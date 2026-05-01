from django.db import models
from django.utils.translation import gettext_lazy as _
from system.models.mixins import OrderableMixin, TimestampMixin


class CardGridBlock(TimestampMixin):
    heading = models.CharField(max_length=255, blank=True)
    intro = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.heading or "Card grid"

    class Meta:
        verbose_name = _("Блок: карточки")
        verbose_name_plural = _("Блоки: карточки")


class CardItem(OrderableMixin):
    block = models.ForeignKey(CardGridBlock, on_delete=models.CASCADE, related_name="items")
    eyebrow = models.CharField(max_length=128, blank=True)
    title = models.CharField(max_length=255)
    text = models.TextField(blank=True)
    image = models.ImageField(upload_to="content/cards/", blank=True, null=True)
    url = models.CharField(max_length=255, blank=True)

    def __str__(self) -> str:
        return self.title

    class Meta(OrderableMixin.Meta):
        verbose_name = _("Карточка")
        verbose_name_plural = _("Карточки")
