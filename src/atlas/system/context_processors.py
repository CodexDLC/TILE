from typing import Any

from django.conf import settings
from django.http import HttpRequest
from django.urls import translate_url
from django.utils.translation import get_language
from features.places.models import Country

from .models import EmailSettings, SiteSettings


def email_settings(request: HttpRequest) -> dict[str, Any]:
    return {"email_settings": EmailSettings.load()}


def site_context(request: HttpRequest) -> dict[str, Any]:
    countries = list(Country.objects.filter(page__is_published=True).select_related("page").order_by("name"))
    active_country = _get_active_country(request, countries)
    return {
        "public_brand": "TALE",
        "SITE_NAME": "TALE",
        "public_brand_full": "Travel Atlas of Local Experiences",
        "active_locale": get_language(),
        "LANGUAGES": settings.LANGUAGES,
        "language_switcher": _get_language_switcher(request),
        "nav_is_home": request.resolver_match and request.resolver_match.url_name == "home",
        "nav_is_stories": request.resolver_match and request.resolver_match.url_name == "places-search",
        "nav_is_contacts": request.resolver_match and request.resolver_match.url_name == "contacts",
        "nav_active_country": active_country,
        "nav_countries": countries,
        "nav_regions_country": active_country,
        "site_settings": SiteSettings.load(),
    }




def _get_language_switcher(request: HttpRequest) -> list[dict[str, str | bool]]:
    active_language = get_language()
    is_preview = (
        request.resolver_match
        and request.resolver_match.namespace == "cabinet"
        and request.resolver_match.url_name == "article_preview"
    )
    return [
        {
            "code": code,
            "label": label,
            "url": _language_url(request, code, is_preview=is_preview),
            "is_active": code == active_language,
        }
        for code, label in settings.LANGUAGES
    ]


def _language_url(request: HttpRequest, language: str, *, is_preview: bool) -> str:
    if is_preview:
        query = request.GET.copy()
        query["language"] = language
        return f"{request.path}?{query.urlencode()}"

    path = request.path
    localized_path = path if path.startswith("/cabinet/") else translate_url(path, language)
    query = request.META.get("QUERY_STRING", "")
    return f"{localized_path}?{query}" if query else localized_path
def _get_active_country(request: HttpRequest, countries: list[Country]) -> Country | None:
    request_path = request.path
    for country in countries:
        country_path = country.page.absolute_path
        if request_path == country_path or request_path.startswith(country_path):
            return country
    return None
