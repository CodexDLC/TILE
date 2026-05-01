from __future__ import annotations

from typing import Any

from django.db.models import Count
from django.http import Http404

from features.content.models import Page, PageBlockSlot
from features.places.models import City, Country, Place, Region


def normalize_page_path(path: str | None) -> str:
    return (path or "").strip("/")


def get_page_by_path(path: str | None, locale: str | None = None) -> Page:
    normalized = normalize_page_path(path)
    try:
        return Page.objects.get(path=normalized, is_published=True)
    except Page.DoesNotExist as exc:
        raise Http404("Page not found") from exc


def get_homepage(locale: str | None = None) -> Page:
    try:
        return Page.objects.get(page_type=Page.PageType.HOME, path="", is_published=True)
    except Page.DoesNotExist:
        return get_page_by_path("", locale=locale)


def get_page_blocks_resolved(page: Page) -> list[PageBlockSlot]:
    slots = list(page.block_slots.select_related("content_type").order_by("order", "id"))
    for slot in slots:
        slot.resolved_block = slot.content_object
    return slots


def get_page_context(page: Page) -> dict[str, Any]:
    slots = get_page_blocks_resolved(page)
    blocks_by_type: dict[str, list[Any]] = {}
    for slot in slots:
        block = getattr(slot, "resolved_block", slot.content_object)
        if block is not None:
            blocks_by_type.setdefault(slot.block_type, []).append(block)

    domain_object = _get_page_domain_object(page)
    context = {
        "page": page,
        "slots": slots,
        "blocks_by_type": blocks_by_type,
        "hero": _first_block(blocks_by_type, "hero"),
        "rich_texts": blocks_by_type.get("rich_text", []),
        "pull_quotes": blocks_by_type.get("pull_quote", []),
        "facts_lists": blocks_by_type.get("facts_list", []),
        "card_grids": blocks_by_type.get("card_grid", []),
        "cta_strips": blocks_by_type.get("cta_strip", []),
        "tabs_blocks": blocks_by_type.get("tabs", []),
        "related_places_blocks": blocks_by_type.get("related_places", []),
        "domain_object": domain_object,
    }
    if page.page_type == Page.PageType.HOME:
        context.update(_get_home_landing_context())
    if page.page_type == Page.PageType.COUNTRY and domain_object is not None:
        context.update(_get_country_page_context(domain_object))
    return context


def get_page_template(page: Page) -> str:
    if page.template_hint:
        return page.template_hint
    return f"content/page_{page.page_type}.html"


def _first_block(blocks_by_type: dict[str, list[Any]], block_type: str) -> Any:
    blocks = blocks_by_type.get(block_type, [])
    return blocks[0] if blocks else None


def _get_page_domain_object(page: Page) -> Any:
    for related_name in ("country", "region", "city", "place"):
        if hasattr(page, related_name):
            return getattr(page, related_name)
    return None


def _get_home_landing_context() -> dict[str, Any]:
    countries = list(
        Country.objects.filter(page__is_published=True)
        .select_related("page")
        .prefetch_related("regions")
        .order_by("name")
    )
    regions = list(
        Region.objects.filter(page__is_published=True)
        .select_related("country", "page")
        .prefetch_related("cities")
        .annotate(place_count=Count("cities__places"))
        .order_by("country__name", "name")[:16]
    )
    cities = list(
        City.objects.filter(page__is_published=True)
        .select_related("region__country", "page")
        .prefetch_related("places")
        .order_by("region__country__name", "region__name", "name")[:8]
    )
    places = list(
        Place.objects.filter(page__is_published=True)
        .select_related("city__region__country", "page")
        .order_by("city__region__country__name", "city__region__name", "city__name", "name")[:8]
    )
    return {
        "home_countries": countries,
        "home_featured_country": _get_featured_country(countries),
        "home_regions": regions,
        "home_cities": cities,
        "home_places": places,
    }


def _get_featured_country(countries: list[Country]) -> Country | None:
    return next((country for country in countries if country.slug == "germany"), countries[0] if countries else None)


def _get_country_page_context(country: Country) -> dict[str, Any]:
    regions = list(
        Region.objects.filter(country=country, page__is_published=True)
        .select_related("country", "page")
        .prefetch_related("cities")
        .annotate(place_count=Count("cities__places"))
        .order_by("name")
    )
    return {"country_regions": regions}
