from unittest.mock import patch

from django.test import TestCase
from features.content.models import FactItem, FactsListBlock, Page, PageBlockSlot, RichTextBlock
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

    def test_switching_countries_scopes_shelves_regions_and_search(self):
        austria = Country.objects.create(slug="austria", name_en="Austria", name_ru="Австрия")
        vienna = Region.objects.create(country=austria, slug="vienna", name_en="Vienna")
        self.city("magdeburg")
        self.city("vienna-city", region=vienna)

        germany = self.client.get("/ru/")
        self.assertContains(germany, 'href="/ru/?country=germany#cities" aria-current="true">Германия</a>')
        self.assertContains(germany, 'href="/ru/?country=austria#cities">Австрия</a>')
        self.assertContains(germany, 'href="/ru/magdeburg/"')
        self.assertNotContains(germany, 'href="/ru/vienna-city/"')

        austria = self.client.get("/ru/", {"country": "austria", "region": self.region.pk})
        self.assertContains(austria, 'href="/ru/?country=austria#cities" aria-current="true">Австрия</a>')
        self.assertContains(austria, 'href="/ru/vienna-city/"')
        self.assertNotContains(austria, 'href="/ru/magdeburg/"')
        self.assertEqual(austria.context["library_regions"], [vienna])
        self.assertIsNone(austria.context["library_in_progress"])
        self.assertEqual(self.client.get("/", {"region": vienna.pk}).context["library_country"], "austria")
        no_matches = self.client.get("/", {"country": "austria", "city": "magdeburg"})
        self.assertContains(no_matches, 'href="/?country=austria#cities">Reset filters')
        self.assertEqual(no_matches.context["library_page"].paginator.count, 0)

    def test_special_covers_remain_visible_with_few_published_stories(self):
        self.city("magdeburg")
        self.city("quedlinburg")
        response = self.client.get("/")
        self.assertNotContains(response, 'class="library-countries"')
        self.assertContains(response, "images/library/magdeburg.jpg")
        self.assertContains(response, "images/library/quedlinburg.jpg")

    def test_city_hides_only_unchanged_demonstration_blocks(self):
        city = self.city("berlin")
        city.intro_en = "City introduction"
        city.save()
        introduction = RichTextBlock.objects.create(
            heading_en="berlin, a first city chapter.", body_en=city.intro_en
        )
        facts = FactsListBlock.objects.create(
            heading_en="City anchors",
            intro_en="A minimal starter layer before the city receives a fuller editorial treatment.",
        )
        for order, (label, value, note) in enumerate(
            (
                ("Country", city.region.country.name_en, ""),
                ("Region", city.region.name_en, ""),
                ("Editorial status", "Starter city page", "Places can be expanded from here."),
            )
        ):
            FactItem.objects.create(block=facts, order=order, label_en=label, value_en=value, note_en=note)
        PageBlockSlot.objects.create(page=city.page, content_object=introduction)
        PageBlockSlot.objects.create(page=city.page, content_object=facts)
        authored = FactsListBlock.objects.create(heading_en="City anchors", intro_en="Author's city guide")
        PageBlockSlot.objects.create(page=city.page, content_object=authored)

        response = self.client.get(city.page.absolute_path)
        self.assertContains(response, "City introduction", count=1)
        self.assertContains(response, "City anchors", count=1)
        self.assertNotContains(response, "a first city chapter")
        self.assertNotContains(response, "Starter city page")
        self.assertContains(response, "Author&#x27;s city guide")

        introduction.body_ru = "Авторское дополнение"
        introduction.save()
        self.assertContains(self.client.get("/ru/berlin/"), "Авторское дополнение")

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
        Page.objects.create(parent=city.page, page_type="story", slug="draft", title_en="Unpublished chapter")
        notes = RichTextBlock.objects.create(body_en="Additional city notes")
        PageBlockSlot.objects.create(page=city.page, content_object=notes)

        library = self.client.get("/")
        book = library.context["library_shelves"][0]["books"][0]
        self.assertEqual(book["article_count"], 2)
        detail = self.client.get(city.page.absolute_path)
        self.assertEqual(set(detail.context["city_articles"]), {station, direct})
        self.assertContains(detail, "Table of contents")
        self.assertContains(detail, 'href="/station/"')
        self.assertContains(detail, "Additional city notes")
        self.assertNotContains(detail, "Unpublished chapter")
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
