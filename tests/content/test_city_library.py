from unittest.mock import patch

from django.test import TestCase
from features.content.models import Page
from features.places.models import City, Country, Place, Region


class CityLibraryTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Page.objects.create(page_type="home", slug="", title_en="Home", is_published=True)
        country = Country.objects.create(slug="germany", name_en="Germany")
        cls.region = Region.objects.create(country=country, slug="saxony-anhalt", name_en="Saxony-Anhalt")
        cls.other_region = Region.objects.create(country=country, slug="saxony", name_en="Saxony")

    def city(self, slug, region=None, published=True):
        page = Page.objects.create(page_type="city", slug=slug, title_en=slug, is_published=published)
        return City.objects.create(region=region or self.region, page=page, slug=slug, name_en=slug)

    def test_special_covers_remain_visible_with_few_published_stories(self):
        self.city("magdeburg")
        self.city("quedlinburg")
        response = self.client.get("/")
        self.assertContains(response, "images/library/magdeburg.jpg")
        self.assertContains(response, "images/library/quedlinburg.jpg")

    def test_horizontal_book_advances_when_the_announced_city_is_published(self):
        dessau = self.city("dessau", published=False)
        self.city("magdeburg")
        queue = (("germany", "dessau", "Dessau"), ("germany", "next", "Next city"))

        with patch("features.places.selectors.library.ANNOUNCED_CITIES", queue):
            response = self.client.get("/")
            self.assertEqual(response.context["library_in_progress"], "Dessau")
            self.assertNotContains(response, 'href="/dessau/"')
            self.assertIsNone(self.client.get("/", {"city": "magdeburg"}).context["library_in_progress"])

            dessau.page.is_published = True
            dessau.page.save()
            response = self.client.get("/")
            self.assertEqual(response.context["library_in_progress"], "Next city")
            self.assertContains(response, 'href="/dessau/"')

    def test_standalone_station_story_appears_in_city_with_its_existing_address(self):
        city = self.city("kothen")
        station = Page.objects.create(page_type="story", slug="station", title_en="Station", is_published=True)
        direct = Page.objects.create(
            parent=city.page, page_type="place", slug="square", title_en="Square", is_published=True
        )
        Place.objects.create(city=city, page=station, slug="station", name_en="Station")
        Place.objects.create(city=city, page=direct, slug="square", name_en="Square")

        library = self.client.get("/")
        book = library.context["library_shelves"][0]["books"][0]
        self.assertEqual(book["article_count"], 2)
        detail = self.client.get(city.page.absolute_path)
        self.assertEqual(set(detail.context["city_articles"]), {station, direct})
        self.assertContains(detail, 'href="/station/"')
        self.assertEqual(self.client.get("/station/").status_code, 200)

    def test_library_counts_only_published_stories_and_places(self):
        city = self.city("magdeburg")
        for kind, published, slug in (
            ("story", True, "story"),
            ("place", True, "place"),
            ("story", False, "draft"),
            ("static", True, "other"),
        ):
            Page.objects.create(parent=city.page, page_type=kind, slug=slug, title_en=slug, is_published=published)
        self.city("hidden-city", published=False)

        response = self.client.get("/")

        book = response.context["library_shelves"][0]["books"][0]
        self.assertEqual(book["article_count"], 2)
        self.assertEqual(response.context["library_total"], 1)
        self.assertNotContains(response, "hidden-city")
        self.assertContains(response, f'href="{city.page.absolute_path}"')

    def test_city_search_matches_names_in_other_languages_and_region_filter(self):
        city = self.city("magdeburg")
        city.name_ru = "Магдебург"
        city.save()
        self.city("dresden", region=self.other_region)

        response = self.client.get("/ru/", {"city": "Магде", "region": self.region.pk})

        self.assertEqual(response.context["library_page"].paginator.count, 1)
        self.assertContains(response, 'href="/ru/magdeburg/"')
        self.assertNotContains(response, 'href="/ru/dresden/"')

    def test_catalog_paginates_without_losing_filters(self):
        for number in range(540):
            self.city(f"city-{number:02}")
        response = self.client.get("/", {"region": self.region.pk})
        self.assertEqual(len(response.context["library_page"]), 24)
        rows = response.context["library_shelves"][0]["rows"]
        self.assertEqual([len(row) for row in rows], [6, 6, 6, 6])
        self.assertEqual(len({book["city"].pk for row in rows for book in row}), 24)
        self.assertContains(response, f"region={self.region.pk}&amp;page=2")
        second = self.client.get("/", {"region": self.region.pk, "page": 2})
        self.assertEqual(len(second.context["library_page"]), 24)
        self.assertEqual(second.context["library_page"].paginator.num_pages, 23)
        last = self.client.get("/", {"region": self.region.pk, "page": 23})
        self.assertEqual(len(last.context["library_page"]), 12)

    def test_no_matches_and_invalid_region_have_recovery(self):
        self.city("magdeburg")
        response = self.client.get("/", {"city": "unknown", "region": "invalid"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No cities found")
        self.assertContains(response, "Reset filters")
