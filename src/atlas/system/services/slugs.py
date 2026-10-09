from __future__ import annotations

from typing import Any

from codex_core.common.text import transliterate
from django.db import models
from django.utils.text import slugify


def build_slug(value: str, *, fallback: str = "item", max_length: int = 255) -> str:
    slug = slugify(transliterate(value or ""))[:max_length].strip("-")
    return slug or fallback


def unique_slug(
    model: type[models.Model],
    value: str,
    *,
    scope: dict[str, Any] | None = None,
    exclude_pk: Any = None,
    slug_field: str = "slug",
    fallback: str = "item",
    max_length: int = 255,
) -> str:
    base_slug = build_slug(value, fallback=fallback, max_length=max_length)
    filters = dict(scope or {})
    filters[slug_field] = base_slug

    queryset = model._default_manager.filter(**filters)
    if exclude_pk is not None:
        queryset = queryset.exclude(pk=exclude_pk)
    if not queryset.exists():
        return base_slug

    suffix = 2
    while True:
        suffix_text = f"-{suffix}"
        candidate = f"{base_slug[: max_length - len(suffix_text)]}{suffix_text}"
        filters[slug_field] = candidate
        queryset = model._default_manager.filter(**filters)
        if exclude_pk is not None:
            queryset = queryset.exclude(pk=exclude_pk)
        if not queryset.exists():
            return candidate
        suffix += 1
