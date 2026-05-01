from typing import Any

from django.http import HttpRequest
from django.utils.translation import get_language
from features.places.models import Country

from .models import EmailSettings, SiteSettings


def email_settings(request: HttpRequest) -> dict[str, Any]:
    return {"email_settings": EmailSettings.load()}


def site_context(request: HttpRequest) -> dict[str, Any]:
    countries = list(Country.objects.filter(page__is_published=True).select_related("page").order_by("name"))
    active_country = _get_active_country(request, countries)
    return {
        "active_locale": get_language(),
        "nav_active_country": active_country,
        "nav_countries": countries,
        "nav_regions_country": active_country,
        "site_settings": SiteSettings.load(),
    }


def _get_active_country(request: HttpRequest, countries: list[Country]) -> Country | None:
    request_path = request.path
    for country in countries:
        country_path = country.page.absolute_path
        if request_path == country_path or request_path.startswith(country_path):
            return country
    return None
