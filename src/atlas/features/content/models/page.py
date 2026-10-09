from __future__ import annotations

from typing import Any

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from system.models.mixins import OrderableMixin, SeoMixin, TimestampMixin
from system.services.slugs import unique_slug


class Page(TimestampMixin, OrderableMixin, SeoMixin):
    class PageType(models.TextChoices):
        HOME = "home", _("Home")
        COUNTRY = "country", _("Country")
        REGION = "region", _("Region")
        CITY = "city", _("City")
        PLACE = "place", _("Place")
        STORY = "story", _("Story")
        STATIC = "static", _("Static")

    parent: Any = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="children",
        blank=True,
        null=True,
        verbose_name=_("Родительская страница"),
    )
    page_type: Any = models.CharField(
        _("Тип страницы"), max_length=32, choices=PageType.choices, default=PageType.STATIC, db_index=True
    )
    slug: Any = models.SlugField("Slug", max_length=255, blank=True, db_index=True)
    path: Any = models.CharField(_("Путь"), max_length=1024, blank=True, db_index=True)
    title: Any = models.CharField(_("Название"), max_length=255)
    intro: Any = models.TextField(_("Вступление"), blank=True)
    template_hint: Any = models.CharField(_("Шаблон"), max_length=128, blank=True, null=True)
    is_published: Any = models.BooleanField(_("Опубликовано"), default=False, db_index=True)
    published_at: Any = models.DateTimeField(_("Дата публикации"), blank=True, null=True)

    class Meta(OrderableMixin.Meta):
        verbose_name = _("Страница")
        verbose_name_plural = _("Страницы")
        constraints = (models.UniqueConstraint(fields=["parent", "slug"], name="content_page_unique_slug_per_parent"),)
        indexes = (
            models.Index(fields=["path", "is_published"]),
            models.Index(fields=["page_type", "is_published"]),
        )

    def __str__(self) -> str:
        return self.title

    @property
    def absolute_path(self) -> str:
        return reverse("home") if not self.path else reverse("page-detail", kwargs={"path": self.path + "/"})

    def build_path(self) -> str:
        if self.page_type == self.PageType.HOME and not self.parent:
            return ""
        parent_path = self.parent.path.strip("/") if self.parent else ""
        slug = self.slug.strip("/")
        return "/".join(part for part in (parent_path, slug) if part)

    def save(self, *args: Any, **kwargs: Any) -> None:
        if not self.slug:
            self.slug = unique_slug(
                type(self),
                self.title,
                scope={"parent": self.parent},
                exclude_pk=self.pk,
                fallback="page",
            )
        if self.is_published and self.published_at is None:
            self.published_at = timezone.now()
        self.path = self.build_path()
        super().save(*args, **kwargs)
