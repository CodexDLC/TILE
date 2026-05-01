from features.places.models import Place


def list_places():
    return Place.objects.select_related("city", "city__region", "city__region__country", "page")


def list_places_for_city(city):
    return list_places().filter(city=city)
