from django.db import models
from django.utils.translation import gettext_lazy as _
from system.models.mixins import OrderableMixin, TimestampMixin


class GalleryBlock(TimestampMixin):
    heading = models.CharField(max_length=255, blank=True)
    intro = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.heading or "Gallery"

    class Meta:
        verbose_name = _("Блок: галерея")
        verbose_name_plural = _("Блоки: галерея")


class GalleryImage(OrderableMixin):
    block = models.ForeignKey(GalleryBlock, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="content/gallery/")
    caption = models.CharField(max_length=255, blank=True)
    alt_text = models.CharField(max_length=255, blank=True)

    def __str__(self) -> str:
        return self.caption or self.alt_text or "Gallery image"

    class Meta(OrderableMixin.Meta):
        verbose_name = _("Изображение галереи")
        verbose_name_plural = _("Изображения галереи")
