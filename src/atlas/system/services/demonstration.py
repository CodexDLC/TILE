from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from django.db import transaction
from features.content.models import (
    CardGridBlock,
    CardItem,
    CtaStripBlock,
    FactItem,
    FactsListBlock,
    GalleryBlock,
    HeroBlock,
    Page,
    PageBlockSlot,
    PullQuoteBlock,
    RelatedPlacesBlock,
    RichTextBlock,
    TabItem,
    TabsBlock,
)
from features.content.services.pages import attach_block, publish_page
from features.places.models import City, Country, Place, PlaceFact, PlaceImage, PlaceSeasonTag, Region, SeasonTag

from system.models.settings import SiteSettings

JsonObject = dict[str, Any]


@transaction.atomic
def load_demonstration_content(fixture_dir: Path) -> dict[str, int]:
    site_settings = _load_json_object(fixture_dir / "site_settings.json")
    place_data = _load_json_object(fixture_dir / "places.json")
    page_data = _load_json_object(fixture_dir / "pages.json")

    _load_site_settings(site_settings)
    domain = _load_place_domain(place_data)
    pages = _load_pages(page_data, domain)
    generated_pages = _ensure_domain_pages(domain)

    return {
        "countries": len(domain["countries"]),
        "regions": len(domain["regions"]),
        "cities": len(domain["cities"]),
        "places": len(domain["places"]),
        "pages": len(pages) + generated_pages,
    }


@transaction.atomic
def reset_demonstration_content() -> None:
    for page in Page.objects.all():
        _delete_existing_blocks(page)
    Page.objects.all().delete()
    Place.objects.all().delete()
    City.objects.all().delete()
    Region.objects.all().delete()
    Country.objects.all().delete()


def _load_json_object(path: Path) -> JsonObject:
    with path.open(encoding="utf-8") as fixture_file:
        data = json.load(fixture_file)
    if not isinstance(data, dict):
        msg = f"Fixture must contain a JSON object: {path}"
        raise ValueError(msg)
    return data


def _load_site_settings(data: JsonObject) -> SiteSettings:
    site_settings = SiteSettings.load()
    changed_fields: list[str] = []

    for field_name, value in data.items():
        if hasattr(site_settings, field_name) and getattr(site_settings, field_name) != value:
            setattr(site_settings, field_name, value)
            changed_fields.append(field_name)

    if changed_fields:
        site_settings.save()

    return site_settings


def _load_place_domain(data: JsonObject) -> dict[str, dict[str, Any]]:
    countries: dict[str, Country] = {}
    regions: dict[str, Region] = {}
    cities: dict[str, City] = {}
    places: dict[str, Place] = {}

    for item in data.get("countries", []):
        country, _created = Country.objects.update_or_create(
            slug=item["slug"],
            defaults=_model_defaults(item, ("name", "intro", "hero_image", "seo_title", "seo_description")),
        )
        countries[country.slug] = country

    for item in data.get("regions", []):
        country = countries[item["country"]]
        region, _created = Region.objects.update_or_create(
            country=country,
            slug=item["slug"],
            defaults=_model_defaults(item, ("name", "intro", "hero_image", "seo_title", "seo_description")),
        )
        regions[region.slug] = region

    for item in data.get("cities", []):
        region = regions[item["region"]]
        city, _created = City.objects.update_or_create(
            region=region,
            slug=item["slug"],
            defaults=_model_defaults(item, ("name", "intro", "hero_image", "seo_title", "seo_description")),
        )
        cities[city.slug] = city

    for item in data.get("places", []):
        city = cities[item["city"]]
        place, _created = Place.objects.update_or_create(
            city=city,
            slug=item["slug"],
            defaults=_model_defaults(
                item,
                (
                    "name",
                    "intro",
                    "hero_image",
                    "long_form_story",
                    "seasonality",
                    "seasonality_text",
                    "latitude",
                    "longitude",
                    "seo_title",
                    "seo_description",
                ),
            ),
        )
        _replace_place_related(place, item)
        places[place.slug] = place

    return {"countries": countries, "regions": regions, "cities": cities, "places": places}


def _model_defaults(item: JsonObject, field_names: tuple[str, ...]) -> JsonObject:
    return {field_name: item[field_name] for field_name in field_names if field_name in item}


def _load_pages(data: JsonObject, domain: dict[str, dict[str, Any]]) -> dict[str, Page]:
    pages: dict[str, Page] = {}

    for item in data.get("pages", []):
        parent = _resolve_parent(item, pages)
        page = _upsert_page(item, parent)
        _link_domain_object(page, item.get("domain"), domain)
        _replace_blocks(page, item.get("blocks", []), domain["places"])
        publish_page(page)
        pages[item["key"]] = page

    return pages


def _ensure_domain_pages(domain: dict[str, dict[str, Any]]) -> int:
    generated = 0

    for country in domain["countries"].values():
        if country.page_id:
            continue
        page = _upsert_page(
            {
                "page_type": Page.PageType.COUNTRY,
                "slug": country.slug,
                "title": country.name,
                "intro": country.intro,
                "seo_title": country.seo_title,
                "seo_description": country.seo_description,
            },
            None,
        )
        country.page = page
        country.save(update_fields=["page", "updated_at"])
        _replace_blocks(page, _country_blocks(country), domain["places"])
        publish_page(page)
        generated += 1

    for region in domain["regions"].values():
        if region.page_id or region.country.page_id is None:
            continue
        page = _upsert_page(
            {
                "page_type": Page.PageType.REGION,
                "slug": region.slug,
                "title": region.name,
                "intro": region.intro,
                "seo_title": region.seo_title,
                "seo_description": region.seo_description,
            },
            region.country.page,
        )
        region.page = page
        region.save(update_fields=["page", "updated_at"])
        _replace_blocks(page, _region_blocks(region), domain["places"])
        publish_page(page)
        generated += 1

    for city in domain["cities"].values():
        if city.page_id or city.region.page_id is None:
            continue
        page = _upsert_page(
            {
                "page_type": Page.PageType.CITY,
                "slug": city.slug,
                "title": city.name,
                "intro": city.intro,
                "seo_title": city.seo_title,
                "seo_description": city.seo_description,
            },
            city.region.page,
        )
        city.page = page
        city.save(update_fields=["page", "updated_at"])
        _replace_blocks(page, _city_blocks(city), domain["places"])
        publish_page(page)
        generated += 1

    for place in domain["places"].values():
        if place.page_id or place.city.page_id is None:
            continue
        page = _upsert_page(
            {
                "page_type": Page.PageType.PLACE,
                "slug": place.slug,
                "title": place.name,
                "intro": place.intro,
                "seo_title": place.seo_title,
                "seo_description": place.seo_description,
            },
            place.city.page,
        )
        place.page = page
        place.save(update_fields=["page", "updated_at"])
        _replace_blocks(page, _place_blocks(place), domain["places"])
        publish_page(page)
        generated += 1

    return generated


def _country_blocks(country: Country) -> list[JsonObject]:
    return [
        {
            "type": "hero",
            "fields": {
                "eyebrow": f"Country / {country.name}",
                "title": country.name,
                "subtitle": country.intro,
                "alignment": "left",
            },
        },
        {
            "type": "rich_text",
            "fields": {
                "heading": f"{country.name}, region by region.",
                "body": country.intro,
            },
        },
        {
            "type": "facts_list",
            "fields": {
                "heading": f"{country.name} at a glance",
                "intro": "A generated country page from the domain tables.",
            },
            "items": [
                {"label": "Editorial status", "value": "Country chapter", "note": ""},
                {"label": "Next layer", "value": "Regions", "note": "Generated from the places domain fixture."},
            ],
        },
    ]


def _region_blocks(region: Region) -> list[JsonObject]:
    return [
        {
            "type": "hero",
            "fields": {
                "eyebrow": f"{region.country.name} / Region",
                "title": region.name,
                "subtitle": region.intro,
                "alignment": "left",
            },
        },
        {
            "type": "rich_text",
            "fields": {
                "heading": f"{region.name}, a first regional chapter.",
                "body": region.intro,
            },
        },
        {
            "type": "facts_list",
            "fields": {
                "heading": "Regional anchors",
                "intro": "A minimal starter layer before the region receives a fuller editorial treatment.",
            },
            "items": [
                {"label": "Country", "value": region.country.name, "note": ""},
                {"label": "Editorial status", "value": "Starter region page", "note": ""},
            ],
        },
    ]


def _city_blocks(city: City) -> list[JsonObject]:
    return [
        {
            "type": "hero",
            "fields": {
                "eyebrow": f"{city.region.name} / City",
                "title": city.name,
                "subtitle": city.intro,
                "alignment": "left",
            },
        },
        {
            "type": "rich_text",
            "fields": {
                "heading": f"{city.name}, a first city chapter.",
                "body": city.intro,
            },
        },
        {
            "type": "facts_list",
            "fields": {
                "heading": "City anchors",
                "intro": "A minimal starter layer before the city receives a fuller editorial treatment.",
            },
            "items": [
                {"label": "Country", "value": city.region.country.name, "note": ""},
                {"label": "Region", "value": city.region.name, "note": ""},
                {
                    "label": "Editorial status",
                    "value": "Starter city page",
                    "note": "Places can be expanded from here.",
                },
            ],
        },
    ]


def _place_blocks(place: Place) -> list[JsonObject]:
    facts = [
        {
            "label": _translated_value(fact, "label"),
            "value": _translated_value(fact, "value"),
            "note": _translated_value(fact, "note"),
        }
        for fact in place.facts.filter(is_visible=True).order_by("order", "pk")
    ]
    if not facts:
        facts = [
            {"label": "City", "value": place.city.name, "note": ""},
            {"label": "Region", "value": place.city.region.name, "note": ""},
        ]

    return [
        {
            "type": "hero",
            "fields": {
                "eyebrow": f"{place.city.name} / Place",
                "title": place.name,
                "subtitle": place.intro,
                "alignment": "left",
            },
        },
        {
            "type": "rich_text",
            "fields": {
                "heading": place.name,
                "body": place.long_form_story or place.intro,
            },
        },
        {
            "type": "facts_list",
            "fields": {
                "heading": "Key facts",
                "intro": place.seasonality_text,
            },
            "items": facts,
        },
    ]


def _translated_value(obj: Any, field_name: str) -> str:
    values = [
        str(getattr(obj, field_name, "") or ""),
        str(getattr(obj, f"{field_name}_en", "") or ""),
        str(getattr(obj, f"{field_name}_de", "") or ""),
        str(getattr(obj, f"{field_name}_ru", "") or ""),
        str(getattr(obj, "__dict__", {}).get(field_name, "") or ""),
    ]
    return next((value for value in values if value), "")


def _replace_place_related(place: Place, item: JsonObject) -> None:
    _replace_place_facts(place, item.get("facts"))
    _replace_place_gallery(place, item.get("gallery"))
    _replace_place_season_tags(place, item.get("season_tags"))


def _replace_place_facts(place: Place, raw_facts: Any) -> None:
    PlaceFact.objects.filter(place=place).delete()
    for order, fact in enumerate(_normalize_facts(raw_facts), start=1):
        PlaceFact.objects.create(place=place, order=order, **fact)


def _normalize_facts(raw_facts: Any) -> list[JsonObject]:
    if isinstance(raw_facts, dict):
        return [
            {"label": str(label).replace("_", " ").title(), "value": str(value), "note": ""}
            for label, value in raw_facts.items()
        ]
    if isinstance(raw_facts, list):
        normalized = []
        for item in raw_facts:
            if isinstance(item, dict):
                normalized.append(
                    {
                        "label": str(item.get("label") or item.get("name") or ""),
                        "value": str(item.get("value") or ""),
                        "note": str(item.get("note") or ""),
                    }
                )
        return [item for item in normalized if item["label"] or item["value"]]
    return []


def _replace_place_gallery(place: Place, raw_gallery: Any) -> None:
    PlaceImage.objects.filter(place=place).delete()
    if not isinstance(raw_gallery, list):
        return
    for order, item in enumerate(raw_gallery, start=1):
        if not isinstance(item, dict) or not item.get("image"):
            continue
        PlaceImage.objects.create(
            place=place,
            order=order,
            image=str(item["image"]),
            caption=str(item.get("caption") or ""),
            alt_text=str(item.get("alt_text") or ""),
            is_cover=bool(item.get("is_cover")),
        )


def _replace_place_season_tags(place: Place, raw_tags: Any) -> None:
    PlaceSeasonTag.objects.filter(place=place).delete()
    if not isinstance(raw_tags, list):
        return
    for order, raw_tag in enumerate(raw_tags, start=1):
        tag_name = str(raw_tag).strip()
        if not tag_name:
            continue
        tag, _created = SeasonTag.objects.get_or_create(
            slug=tag_name.lower().replace(" ", "-"),
            defaults={"name": tag_name.replace("-", " ").title()},
        )
        PlaceSeasonTag.objects.create(place=place, tag=tag, order=order)


def _resolve_parent(item: JsonObject, pages: dict[str, Page]) -> Page | None:
    parent_key = item.get("parent")
    if parent_key and parent_key in pages:
        return pages[parent_key]

    parent_path = item.get("parent_path")
    if parent_path:
        path = "/".join(parent_path)
        return Page.objects.filter(path=path).first()

    return None


def _upsert_page(item: JsonObject, parent: Page | None) -> Page:
    slug = item.get("slug", "")
    expected_path = _expected_path(parent, slug, item["page_type"])
    page = Page.objects.filter(path=expected_path, page_type=item["page_type"]).first()
    if page is None:
        page = Page(path=expected_path, page_type=item["page_type"])

    page.parent = parent
    page.slug = slug
    page.page_type = item["page_type"]
    page.title = item["title"]
    page.intro = item.get("intro", "")
    page.seo_title = item.get("seo_title", "")
    page.seo_description = item.get("seo_description", "")
    page.is_published = True
    page.save()
    return page


def _expected_path(parent: Page | None, slug: str, page_type: str) -> str:
    if page_type == Page.PageType.HOME and not parent:
        return ""
    parent_path = parent.path.strip("/") if parent else ""
    return "/".join(part for part in (parent_path, slug.strip("/")) if part)


def _link_domain_object(page: Page, domain_ref: JsonObject | None, domain: dict[str, dict[str, Any]]) -> None:
    if not domain_ref:
        return

    collection_key = {
        "country": "countries",
        "region": "regions",
        "city": "cities",
        "place": "places",
    }[domain_ref["model"]]
    domain_object = domain[collection_key][domain_ref["slug"]]
    if domain_object.page_id != page.id:
        domain_object.page = page
        domain_object.save(update_fields=["page", "updated_at"])


def _replace_blocks(page: Page, block_specs: list[JsonObject], places: dict[str, Place]) -> None:
    _delete_existing_blocks(page)
    for order, spec in enumerate(block_specs):
        block = _create_block(spec, places)
        attach_block(page, block, order=order, display_variant=spec.get("display_variant", ""))


def _delete_existing_blocks(page: Page) -> None:
    slots = list(page.block_slots.select_related("content_type"))
    for slot in slots:
        content_type = slot.content_type
        object_id = slot.object_id
        block = slot.content_object
        slot.delete()
        if block is None:
            continue
        still_used = PageBlockSlot.objects.filter(content_type=content_type, object_id=object_id).exists()
        if not still_used:
            block.delete()


def _create_block(spec: JsonObject, places: dict[str, Place]) -> object:
    block_type = spec["type"]
    fields = spec.get("fields", {})

    if block_type == "hero":
        return HeroBlock.objects.create(**fields)
    if block_type == "rich_text":
        return RichTextBlock.objects.create(**fields)
    if block_type == "pull_quote":
        return PullQuoteBlock.objects.create(**fields)
    if block_type == "cta_strip":
        return CtaStripBlock.objects.create(**fields)
    if block_type == "gallery":
        return GalleryBlock.objects.create(**fields)
    if block_type == "facts_list":
        return _create_facts_list_block(fields, spec.get("items", []))
    if block_type == "card_grid":
        return _create_card_grid_block(fields, spec.get("items", []))
    if block_type == "tabs":
        return _create_tabs_block(fields, spec.get("items", []))
    if block_type == "related_places":
        return _create_related_places_block(fields, spec.get("places", []), places)

    msg = f"Unsupported demo block type: {block_type}"
    raise ValueError(msg)


def _create_facts_list_block(fields: JsonObject, items: list[JsonObject]) -> FactsListBlock:
    block = FactsListBlock.objects.create(**fields)
    for order, item in enumerate(items):
        FactItem.objects.create(block=block, order=order, **item)
    return block


def _create_card_grid_block(fields: JsonObject, items: list[JsonObject]) -> CardGridBlock:
    block = CardGridBlock.objects.create(**fields)
    for order, item in enumerate(items):
        CardItem.objects.create(block=block, order=order, **item)
    return block


def _create_tabs_block(fields: JsonObject, items: list[JsonObject]) -> TabsBlock:
    block = TabsBlock.objects.create(**fields)
    for order, item in enumerate(items):
        TabItem.objects.create(block=block, order=order, **item)
    return block


def _create_related_places_block(
    fields: JsonObject,
    place_slugs: list[str],
    places: dict[str, Place],
) -> RelatedPlacesBlock:
    block = RelatedPlacesBlock.objects.create(**fields)
    block.places.set([places[slug] for slug in place_slugs])
    return block


__all__ = ["load_demonstration_content", "reset_demonstration_content"]
