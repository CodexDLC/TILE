"""Read-only city catalogue for the home bookshelf; no new content or URLs."""

from itertools import groupby
from urllib.parse import urlencode

from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.utils.translation import gettext_lazy as _

from features.places.models import City, Region

# Only these explicitly announced cities can appear on the horizontal book, in this order.
ANNOUNCED_CITIES = (("germany", "dessau", _("Dessau")),)


def get_city_library(*, query="", region="", page=1):
    query = query.strip()[:120]
    region = int(region) if str(region).isascii() and str(region).isdigit() and len(str(region)) < 10 else None
    cities = City.objects.filter(page__is_published=True, page__page_type="city")
    regions = list(Region.objects.filter(cities__in=cities).distinct().select_related("country").order_by("name", "pk"))
    if region not in {item.pk for item in regions}:
        region = None
    total = cities.count()
    if query:
        cities = cities.filter(Q(name_en__icontains=query) | Q(name_de__icontains=query) | Q(name_ru__icontains=query))
    if region:
        cities = cities.filter(region_id=region)
    cities = (
        cities.select_related("page", "region__country")
        .annotate(
            article_count=Count(
                "page__children",
                filter=Q(page__children__is_published=True, page__children__page_type__in=("story", "place")),
                distinct=True,
            )
            + Count(
                "places__page",
                filter=Q(
                    places__page__is_published=True,
                    places__page__page_type__in=("story", "place"),
                    places__page__parent__isnull=True,
                ),
                distinct=True,
            ),
        )
        .order_by("region__country__name", "region__name", "region_id", "name", "pk")
    )
    catalogue = Paginator(cities, 24).get_page(page)
    shelves = []
    for _, group in groupby(catalogue.object_list, key=lambda city: city.region_id):
        books = [_city_book(city) for city in group]
        shelves.append(
            {
                "region": books[0]["city"].region,
                "books": books,
                "rows": [books[start : start + 6] for start in range(0, len(books), 6)],
            }
        )
    filters = {key: value for key, value in (("city", query), ("region", region)) if value}
    return {
        "library_shelves": shelves,
        "library_page": catalogue,
        "library_total": total,
        "library_regions": regions,
        "library_is_german": {item.country.slug for item in regions} == {"germany"},
        "library_query": query,
        "library_region": region,
        "library_filtered": bool(query or region),
        "library_in_progress": _next_announced_city() if not filters and catalogue.number == 1 else None,
        "library_previous": urlencode({**filters, "page": catalogue.previous_page_number()})
        if catalogue.has_previous()
        else "",
        "library_next": urlencode({**filters, "page": catalogue.next_page_number()}) if catalogue.has_next() else "",
    }


def _next_announced_city():
    if not ANNOUNCED_CITIES:
        return None
    countries, slugs, _titles = zip(*ANNOUNCED_CITIES)
    published = set(
        City.objects.filter(
            page__is_published=True,
            page__page_type="city",
            region__country__slug__in=countries,
            slug__in=slugs,
        ).values_list("region__country__slug", "slug")
    )
    return next((title for country, slug, title in ANNOUNCED_CITIES if (country, slug) not in published), None)


def _city_book(city):
    count = city.article_count
    reliefs = {
        "magdeburg": ("magdeburg.jpg", "cover"),
        "quedlinburg": ("relief-quedlinburg.jpg", "screen"),
        "halle": ("relief-halle.png", "cutout"),
    }
    relief, relief_kind = reliefs.get(city.slug, ("", "")) if city.region.country.slug == "germany" else ("", "")
    cover_art = (
        f"images/library/{city.slug}.{'jfif' if city.slug == 'halle' else 'jpg'}"
        if relief and (city.slug in ("magdeburg", "quedlinburg") or count >= 4)
        else ""
    )
    return {
        "city": city,
        "article_count": count,
        "size": "wide" if count >= 12 else "medium" if count >= 4 or cover_art else "slim",
        "tone": ("wine", "forest", "navy", "ochre")[city.pk % 4],
        "relief": f"images/library/{relief}" if relief else "",
        "relief_kind": relief_kind,
        "cover_art": cover_art,
        "cover_key": city.slug if relief else "",
    }
