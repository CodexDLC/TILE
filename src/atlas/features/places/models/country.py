from django.db import models
from django.utils.translation import gettext_lazy as _
from system.models.mixins import SeoMixin, TimestampMixin


class Country(TimestampMixin, SeoMixin):
    page = models.OneToOneField(
        "content.Page",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="country",
        verbose_name=_("Страница"),
    )
    slug = models.SlugField("Slug", max_length=255, unique=True)
    name = models.CharField(_("Название"), max_length=255)
    hero_image = models.ImageField(_("Hero image"), upload_to="places/countries/", blank=True, null=True)
    intro = models.TextField(_("Вступление"), blank=True)

    class Meta:
        verbose_name = _("Страна")
        verbose_name_plural = _("Страны")
        ordering = ["name"]  # noqa: RUF012

    def __str__(self) -> str:
        return self.name
