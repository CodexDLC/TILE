from django.db import models
from django.utils.translation import gettext_lazy as _
from system.models.mixins import SeoMixin, TimestampMixin
from system.services.slugs import unique_slug


class Place(TimestampMixin, SeoMixin):
    city = models.ForeignKey("places.City", on_delete=models.CASCADE, related_name="places", verbose_name=_("Город"))
    page = models.OneToOneField(
        "content.Page",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="place",
        verbose_name=_("Страница"),
    )
    slug = models.SlugField("Slug", max_length=255)
    name = models.CharField(_("Название"), max_length=255)
    hero_image = models.ImageField(_("Hero image"), upload_to="places/place_heroes/", blank=True, null=True)
    intro = models.TextField(_("Вступление"), blank=True)
    long_form_story = models.TextField(_("История / long-form"), blank=True)
    seasonality = models.CharField(_("Сезонность"), max_length=255, blank=True)
    seasonality_text = models.TextField(_("Текст о сезонности"), blank=True)  # noqa: RUF001
    latitude = models.DecimalField(_("Широта"), max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(_("Долгота"), max_digits=9, decimal_places=6, blank=True, null=True)
    season_tags = models.ManyToManyField(
        "places.SeasonTag",
        through="places.PlaceSeasonTag",
        related_name="places",
        blank=True,
        verbose_name=_("Сезонные теги"),
    )

    class Meta:
        verbose_name = _("Место")
        verbose_name_plural = _("Места")
        ordering = ["city__region__country__name", "city__region__name", "city__name", "name"]  # noqa: RUF012
        constraints = [  # noqa: RUF012
            models.UniqueConstraint(fields=["city", "slug"], name="places_place_unique_slug_per_city"),
        ]

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = unique_slug(
                type(self),
                self.name,
                scope={"city": self.city},
                exclude_pk=self.pk,
                fallback="place",
            )
        super().save(*args, **kwargs)
