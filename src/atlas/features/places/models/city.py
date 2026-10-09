from django.db import models
from django.utils.translation import gettext_lazy as _
from system.models.mixins import SeoMixin, TimestampMixin
from system.services.slugs import unique_slug


class City(TimestampMixin, SeoMixin):
    region = models.ForeignKey(
        "places.Region",
        on_delete=models.CASCADE,
        related_name="cities",
        verbose_name=_("Регион"),
    )
    page = models.OneToOneField(
        "content.Page",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="city",
        verbose_name=_("Страница"),
    )
    slug = models.SlugField("Slug", max_length=255)
    name = models.CharField(_("Название"), max_length=255)
    hero_image = models.ImageField(_("Hero image"), upload_to="places/cities/", blank=True, null=True)
    intro = models.TextField(_("Вступление"), blank=True)

    class Meta:
        verbose_name = _("Город")
        verbose_name_plural = _("Города")
        ordering = ["region__country__name", "region__name", "name"]  # noqa: RUF012
        constraints = [  # noqa: RUF012
            models.UniqueConstraint(fields=["region", "slug"], name="places_city_unique_slug_per_region"),
        ]

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = unique_slug(
                type(self),
                self.name,
                scope={"region": self.region},
                exclude_pk=self.pk,
                fallback="city",
            )
        super().save(*args, **kwargs)
