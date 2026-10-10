"""Read models shared by the author editor and public article pages."""

from django.conf import settings
from django.db.models import Case, IntegerField, Q, Value, When
from django.shortcuts import get_object_or_404
from django.utils.translation import get_language

from features.content.models import Page

ARTICLE_TYPES = (Page.PageType.STORY, Page.PageType.PLACE)


def articles():
    return Page.objects.filter(page_type__in=ARTICLE_TYPES).select_related("parent")


def get_article(pk):
    return get_object_or_404(articles(), pk=pk)


def article_parts(page):
    parts = {"body_block": None, "cover": None, "gallery": None, "slots": []}
    if page is None:
        return parts
    for slot in page.block_slots.select_related("content_type").order_by("order", "pk"):
        block = slot.content_object
        if block is None:
            continue
        parts["slots"].append(slot)
        if slot.block_type == "rich_text" and parts["body_block"] is None:
            parts["body_block"] = block
        if slot.block_type == "gallery" and parts["gallery"] is None:
            parts["gallery"] = block
            parts["cover"] = block.images.order_by("order", "pk").first()
    return parts


def raw_translation(obj, field, language):
    return getattr(obj, f"{field}_{language}", "") or "" if obj is not None else ""


def article_language(page, preferred=None):
    languages = [preferred or get_language(), "ru", "en", "de"]
    parts = article_parts(page)
    place = getattr(page, "place", None)
    body_source = parts["body_block"] or place
    body_field = "body" if parts["body_block"] is not None else "long_form_story"
    for code in dict.fromkeys(languages):
        if not raw_translation(page, "title", code):
            continue
        if body_source is None or raw_translation(body_source, body_field, code):
            return code
    return next((code for code in languages if raw_translation(page, "title", code)), "ru")


def related_articles(page, language=None, limit=4):
    """Offer same-city reading first, then other stories in the interface language."""
    language = language or get_language()
    candidates = (
        articles()
        .filter(is_published=True)
        .exclude(pk=page.pk)
        .exclude(**{f"title_{language}": ""})
        .exclude(**{f"title_{language}__isnull": True})
        .annotate(
            reading_priority=Case(
                When(parent_id=page.parent_id, then=Value(0)),
                default=Value(1),
                output_field=IntegerField(),
            )
        )
        .order_by("reading_priority", "-published_at", "-pk")
    )
    selected = []
    for candidate in candidates:
        if article_language(candidate, preferred=language) == language:
            selected.append(candidate)
        if len(selected) == limit:
            break
    return selected


def editor_initial(page, language):
    if page is None:
        return {"language": language}
    parts = article_parts(page)
    place = getattr(page, "place", None)
    cover = parts["cover"]
    body = raw_translation(parts["body_block"], "body", language)
    if parts["body_block"] is None and place is not None:
        body = raw_translation(place, "long_form_story", language)
    return {
        "language": language,
        "title": raw_translation(page, "title", language),
        "intro": raw_translation(page, "intro", language),
        "body": body,
        "city": page.parent_id if page.parent and page.parent.page_type == "city" else None,
        "seo_title": raw_translation(page, "seo_title", language),
        "seo_description": raw_translation(page, "seo_description", language),
        "caption": raw_translation(cover, "caption", language),
        "alt_text": raw_translation(cover, "alt_text", language),
    }


def search_pages(query):
    pages = Page.objects.filter(is_published=True).exclude(page_type="home").select_related("parent")
    if query:
        conditions = Q()
        for code, _label in settings.LANGUAGES:
            for field in ("title", "intro", "parent__title", "parent__parent__title"):
                conditions |= Q(**{f"{field}_{code}__icontains": query})
        pages = pages.filter(conditions)
    return pages.order_by("-published_at", "-pk")
