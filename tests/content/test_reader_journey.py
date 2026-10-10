from django.test import TestCase
from features.content.models import Page, PageBlockSlot, RichTextBlock
from features.places.models import City, Country, Region


class ReaderJourneyTests(TestCase):
    def story(self, slug, parent=None, published=True, language="en", title=None):
        page = Page.objects.create(
            page_type="story",
            slug=slug,
            parent=parent,
            is_published=published,
            **{f"title_{language}": title or slug},
        )
        body = RichTextBlock.objects.create(**{f"body_{language}": f"Body for {slug}"})
        PageBlockSlot.objects.create(page=page, content_object=body)
        return page

    def test_next_stories_prioritize_same_city_and_fill_from_other_published_stories(self):
        city = Page.objects.create(page_type="city", slug="city", title_en="City", is_published=True)
        current = self.story("current", city)
        sibling = self.story("sibling", city)
        elsewhere = self.story("elsewhere")
        self.story("draft", city, published=False)
        self.story("untranslated", city, language="ru")

        response = self.client.get(current.absolute_path)

        self.assertEqual([item.pk for item in response.context["related_articles"]], [sibling.pk, elsewhere.pk])
        self.assertContains(response, f'href="{elsewhere.absolute_path}"')
        self.assertNotContains(response, 'href="/city/draft/"')
        self.assertNotContains(response, 'href="/city/untranslated/"')

    def test_related_story_links_use_requested_language_and_require_complete_translation(self):
        self.story("current", language="de")
        translated = self.story("translated", language="de", title="Deutscher Nachfolger")
        incomplete = self.story("incomplete", language="ru")
        incomplete.title_de = "Incomplete German"
        incomplete.save()
        self.story("only-russian", language="ru")

        response = self.client.get("/de/current/")

        self.assertEqual([item.pk for item in response.context["related_articles"]], [translated.pk])
        self.assertContains(response, 'href="/de/translated/"')
        self.assertContains(response, "Deutscher Nachfolger")
        self.assertNotContains(response, "Incomplete German")

    def test_russian_story_links_stay_on_russian_route(self):
        self.story("current", language="ru")
        related = self.story("related", language="ru")

        response = self.client.get("/ru/current/")

        self.assertEqual([item.pk for item in response.context["related_articles"]], [related.pk])
        self.assertContains(response, 'href="/ru/related/"')

    def test_city_stories_precede_long_city_content_and_exclude_drafts(self):
        city = Page.objects.create(page_type="city", slug="city", title_en="City", is_published=True)
        block = RichTextBlock.objects.create(body_en="Long city history")
        PageBlockSlot.objects.create(page=city, content_object=block)
        self.story("published-story", city)
        self.story("draft-story", city, published=False)

        response = self.client.get("/city/")
        html = response.content.decode()

        self.assertLess(html.index("published-story"), html.index("Long city history"))
        self.assertNotContains(response, "draft-story")

    def test_search_cards_label_geography_and_route_to_the_correct_page(self):
        for page_type in ("city", "region", "country"):
            Page.objects.create(
                page_type=page_type,
                slug=page_type,
                title_en=f"Result {page_type}",
                is_published=True,
            )
        self.story("story", title="Result story")
        self.story("draft", title="Result draft", published=False)

        response = self.client.get("/places/search/?q=Result")

        for page_type in ("city", "region", "country"):
            self.assertContains(response, f'href="/{page_type}/"')
            self.assertContains(response, f"Open {page_type}")
        self.assertContains(response, "Read the story")
        self.assertNotContains(response, "Result draft")

    def test_home_city_selection_precedes_stories_and_excludes_unpublished_city(self):
        Page.objects.create(page_type="home", slug="", title_en="Home", is_published=True)
        country = Country.objects.create(name_en="Country", slug="country")
        region = Region.objects.create(country=country, name_en="Region", slug="region")
        for slug, published in (("published-city", True), ("draft-city", False)):
            page = Page.objects.create(page_type="city", slug=slug, title_en=slug, is_published=published)
            City.objects.create(region=region, page=page, slug=slug, name_en=slug)
        self.story("latest-story")

        response = self.client.get("/")
        html = response.content.decode()

        self.assertLess(html.index('id="cities"'), html.index("Stories for your walk"))
        self.assertContains(response, 'href="/published-city/"')
        self.assertNotContains(response, "draft-city")
