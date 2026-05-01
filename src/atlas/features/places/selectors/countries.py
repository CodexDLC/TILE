from features.places.models import Country


def list_countries():
    return Country.objects.select_related("page").prefetch_related("regions")
