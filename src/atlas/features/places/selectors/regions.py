from features.places.models import Region


def list_regions_for_country(country):
    return Region.objects.filter(country=country).select_related("country", "page").prefetch_related("cities")
