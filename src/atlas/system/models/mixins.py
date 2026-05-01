from __future__ import annotations

from typing import Any

from codex_django.core.mixins.models import ActiveMixin as CodexActiveMixin
from codex_django.core.mixins.models import OrderableMixin, SeoMixin, SlugMixin, TimestampMixin
from django.db import models
from django.utils.text import slugify


class ActiveMixin(CodexActiveMixin):
    is_published = models.BooleanField(default=False, db_index=True)
    is_planned = models.BooleanField(default=False, db_index=True)

    class Meta:
        abstract = True


class ParentScopedSlugMixin(models.Model):
    slug = models.SlugField(max_length=255, blank=True, db_index=True)

    class Meta:
        abstract = True

    def build_slug_from(self, value: str) -> str:
        return slugify(value)[:255]

    def ensure_slug(self, source: str) -> None:
        if not self.slug:
            self.slug = self.build_slug_from(source)

    @classmethod
    def slug_exists(cls, slug: str, parent: Any = None, exclude_pk: Any = None) -> bool:
        queryset = cls.objects.filter(slug=slug, parent=parent)
        if exclude_pk:
            queryset = queryset.exclude(pk=exclude_pk)
        return queryset.exists()


__all__ = [
    "ActiveMixin",
    "OrderableMixin",
    "ParentScopedSlugMixin",
    "SeoMixin",
    "SlugMixin",
    "TimestampMixin",
]
