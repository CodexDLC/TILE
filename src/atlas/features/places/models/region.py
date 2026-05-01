from django.db import models
from django.utils.translation import gettext_lazy as _
from system.models.mixins import SeoMixin, TimestampMixin


class Region(TimestampMixin, SeoMixin):
    country = models.ForeignKey(
        "places.Country", on_delete=models.CASCADE, related_name="regions", verbose_name=_("Страна")
    )
    page = models.OneToOneField(
        "content.Page", on_delete=models.SET_NULL, blank=True, null=True, related_name="region", verbose_name=_("Страница")
    )
    slug = models.SlugField("Slug", max_length=255)
    name = models.CharField(_("Название"), max_length=255)
    hero_image = models.ImageField(_("Hero image"), upload_to="places/regions/", blank=True, null=True)
    intro = models.TextField(_("Вступление"), blank=True)

    class Meta:
        verbose_name = _("Регион")
        verbose_name_plural = _("Регионы")
        ordering = ["country__name", "name"]  # noqa: RUF012
        constraints = [  # noqa: RUF012
            models.UniqueConstraint(fields=["country", "slug"], name="places_region_unique_slug_per_country"),
        ]

    def __str__(self) -> str:
        return self.name
