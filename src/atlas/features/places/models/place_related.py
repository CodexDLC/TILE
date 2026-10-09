from typing import ClassVar

from django.db import models
from django.utils.translation import gettext_lazy as _
from system.models.mixins import OrderableMixin, TimestampMixin
from system.services.slugs import build_slug


class PlaceFact(OrderableMixin):
    place = models.ForeignKey("places.Place", on_delete=models.CASCADE, related_name="facts", verbose_name=_("Место"))
    label = models.CharField(_("Название"), max_length=128)
    value = models.CharField(_("Значение"), max_length=255)
    note = models.CharField(_("Примечание"), max_length=255, blank=True)
    icon = models.CharField(_("Иконка"), max_length=64, blank=True)
    is_visible = models.BooleanField(_("Показывать"), default=True)

    def __str__(self) -> str:
        return self.label

    class Meta(OrderableMixin.Meta):
        verbose_name = _("Факт места")
        verbose_name_plural = _("Факты места")


class PlaceImage(OrderableMixin):
    place = models.ForeignKey("places.Place", on_delete=models.CASCADE, related_name="gallery", verbose_name=_("Место"))
    image = models.ImageField(_("Изображение"), upload_to="places/place_gallery/")
    caption = models.CharField(_("Подпись"), max_length=255, blank=True)
    alt_text = models.CharField(_("Alt text"), max_length=255, blank=True)
    is_cover = models.BooleanField(_("Обложка"), default=False)

    def __str__(self) -> str:
        return self.caption or self.alt_text or str(_("Изображение места"))

    class Meta(OrderableMixin.Meta):
        verbose_name = _("Изображение места")
        verbose_name_plural = _("Изображения места")


class SeasonTag(TimestampMixin):
    slug = models.SlugField(_("Slug"), max_length=128, unique=True)
    name = models.CharField(_("Название"), max_length=128)
    color = models.CharField(_("Цвет"), max_length=32, blank=True)
    icon = models.CharField(_("Иконка"), max_length=64, blank=True)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = build_slug(self.name, fallback="season")
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Сезонный тег")
        verbose_name_plural = _("Сезонные теги")
        ordering: ClassVar[list[str]] = ["name"]


class PlaceSeasonTag(OrderableMixin):
    place = models.ForeignKey(
        "places.Place",
        on_delete=models.CASCADE,
        related_name="season_tag_links",
        verbose_name=_("Место"),
    )
    tag = models.ForeignKey(
        "places.SeasonTag",
        on_delete=models.CASCADE,
        related_name="place_links",
        verbose_name=_("Тег"),  # noqa: RUF001
    )

    def __str__(self) -> str:
        return f"{self.place} / {self.tag}"

    class Meta(OrderableMixin.Meta):
        verbose_name = _("Сезонный тег места")
        verbose_name_plural = _("Сезонные теги мест")
        constraints: ClassVar[list[models.BaseConstraint]] = [
            models.UniqueConstraint(fields=["place", "tag"], name="places_place_season_tag_unique"),
        ]
