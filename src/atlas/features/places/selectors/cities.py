from features.places.models import City


def list_cities_for_region(region):
    return (
        City.objects.filter(region=region)
        .select_related("region", "region__country", "page")
        .prefetch_related("places")
    )
