from __future__ import annotations

from collections.abc import Iterable

from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.utils import timezone

from features.content.models import Page, PageBlockSlot


@transaction.atomic
def publish_page(page: Page) -> Page:
    page.is_published = True
    page.published_at = page.published_at or timezone.now()
    page.save(update_fields=["is_published", "published_at", "path", "updated_at"])
    return page


@transaction.atomic
def reorder_blocks(page: Page, slot_ids: Iterable[int]) -> None:
    for order, slot_id in enumerate(slot_ids):
        PageBlockSlot.objects.filter(page=page, id=slot_id).update(order=order)


@transaction.atomic
def attach_block(page: Page, block: object, order: int | None = None, display_variant: str = "") -> PageBlockSlot:
    if order is None:
        last_order = PageBlockSlot.objects.filter(page=page).order_by("-order").values_list("order", flat=True).first()
        order = 0 if last_order is None else last_order + 1

    return PageBlockSlot.objects.create(
        page=page,
        content_type=ContentType.objects.get_for_model(block),
        object_id=block.pk,
        order=order,
        display_variant=display_variant,
    )
