"""Atomic author operations; page blocks remain the content source of truth."""

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.utils.translation import override

from features.content.models import GalleryBlock, GalleryImage, Page, PageBlockSlot, RichTextBlock
from features.content.selectors.articles import article_parts


def require_author(user, action):
    if not user.is_active or not user.is_staff or not user.has_perm(f"content.{action}_page"):
        raise PermissionDenied


def _private_block(page, block):
    content_type = ContentType.objects.get_for_model(block)
    slots = PageBlockSlot.objects.filter(content_type=content_type, object_id=block.pk)
    if slots.exclude(page=page).exists():
        old_id = block.pk
        photos = list(block.images.all()) if isinstance(block, GalleryBlock) else []
        block.pk = None
        block.save()
        for photo in photos:
            photo.pk = None
            photo.block = block
            photo.save()
        PageBlockSlot.objects.filter(page=page, content_type=content_type, object_id=old_id).update(object_id=block.pk)
    return block


def _attach(page, block, order):
    PageBlockSlot.objects.create(page=page, content_object=block, order=order)


@transaction.atomic
def save_article(*, user, data, page=None, publish=False):
    require_author(user, "change" if page else "add")
    if publish:
        require_author(user, "change")
    language = data["language"]
    if page:
        page = Page.objects.select_for_update().get(pk=page.pk)
    else:
        page = Page(page_type=Page.PageType.STORY, parent=data.get("city"))
    with override(language):
        for field in ("title", "intro", "seo_title", "seo_description"):
            setattr(page, f"{field}_{language}", data.get(field, ""))
        if publish:
            page.is_published = True
        page.save()
        parts = article_parts(page)
        body = parts["body_block"]
        if body is None:
            body = RichTextBlock.objects.create()
            _attach(page, body, 10)
        body = _private_block(page, body)
        setattr(body, f"body_{language}", data.get("body", ""))
        body.save()
        gallery = parts["gallery"]
        if gallery:
            gallery = _private_block(page, gallery)
        elif data.get("image") or data.get("additional_images"):
            gallery = GalleryBlock.objects.create()
            _attach(page, gallery, 20)
        cover = gallery.images.order_by("order", "pk").first() if gallery else None
        if data.get("image"):
            cover = cover or GalleryImage(block=gallery)
            cover.image = data["image"]
        if cover:
            for field in ("caption", "alt_text"):
                setattr(cover, f"{field}_{language}", data.get(field, ""))
            cover.save()
        for image in data.get("additional_images", []):
            GalleryImage.objects.create(block=gallery, image=image, **{f"alt_text_{language}": data["title"]})
    return page


@transaction.atomic
def unpublish_article(*, user, page):
    require_author(user, "change")
    Page.objects.filter(pk=page.pk).update(is_published=False)
