from django.db import models
from django.utils.translation import gettext_lazy as _
from system.models.mixins import TimestampMixin


class HeroBlock(TimestampMixin):
    class Alignment(models.TextChoices):
        LEFT = "left", _("Left")
        CENTER = "center", _("Center")

    eyebrow = models.CharField(max_length=128, blank=True)
    title = models.CharField(max_length=255)
    subtitle = models.TextField(blank=True)
    image = models.ImageField(upload_to="content/hero/", blank=True, null=True)
    cta_label = models.CharField(max_length=128, blank=True)
    cta_url = models.CharField(max_length=255, blank=True)
    secondary_cta_label = models.CharField(max_length=128, blank=True)
    secondary_cta_url = models.CharField(max_length=255, blank=True)
    alignment = models.CharField(max_length=16, choices=Alignment.choices, default=Alignment.LEFT)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = _("Блок: Hero")
        verbose_name_plural = _("Блоки: Hero")
