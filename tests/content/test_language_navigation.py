# ruff: noqa: S106
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from features.content.models import Page, PageBlockSlot, RichTextBlock


class LanguageNavigationTests(TestCase):
    def test_search_language_links_preserve_query_and_pagination(self):
        response = self.client.get("/de/places/search/?q=alps&page=2")

        self.assertContains(response, 'href="/places/search/?q=alps&amp;page=2"')
        self.assertContains(response, 'href="/ru/places/search/?q=alps&amp;page=2"')
        self.assertContains(response, 'href="/de/places/search/?q=alps&amp;page=2" lang="de" aria-current="true"')
        self.assertTrue(response.context["nav_is_stories"])

    def test_contacts_and_story_switch_to_the_same_localized_route(self):
        contacts = self.client.get("/de/contacts/")
        self.assertContains(contacts, 'href="/contacts/"')
        self.assertContains(contacts, 'href="/ru/contacts/"')
        self.assertTrue(contacts.context["nav_is_contacts"])

        story = Page.objects.create(title_en="English title", page_type="story", slug="story", is_published=True)
        body = RichTextBlock.objects.create(body_en="English body")
        PageBlockSlot.objects.create(page=story, content_object=body)

        response = self.client.get("/de/story/")
        self.assertContains(response, 'href="/story/"')
        self.assertContains(response, 'href="/ru/story/"')

    def test_article_falls_back_as_one_language_when_body_is_missing(self):
        story = Page.objects.create(
            title_de="Deutscher Titel", title_ru="Русский заголовок", page_type="story", slug="story", is_published=True
        )
        body = RichTextBlock.objects.create(body_ru="Русский текст")
        PageBlockSlot.objects.create(page=story, content_object=body)

        response = self.client.get("/de/story/")

        self.assertContains(response, "Русский заголовок")
        self.assertContains(response, "Русский текст")
        self.assertEqual(response.context["article_language"], "ru")

    def test_preview_language_links_stay_on_the_protected_preview_route(self):
        author = get_user_model().objects.create_superuser(
            username="author", email="author@example.test", password="test-password"
        )
        self.client.force_login(author)
        story = Page.objects.create(title_ru="Черновик", page_type="story", slug="draft")
        body = RichTextBlock.objects.create(body_ru="Текст черновика")
        PageBlockSlot.objects.create(page=story, content_object=body)

        preview_url = reverse("cabinet:article_preview", args=[story.pk])
        response = self.client.get(preview_url + "?language=ru")

        self.assertContains(response, f'href="{preview_url}?language=de"')
        self.assertContains(response, f'href="{preview_url}?language=en"')
        self.assertNotContains(response, 'href="/draft/"')

    def test_grid_and_map_redirect_to_search_without_losing_query(self):
        for path in ("/de/places/grid/?q=alps&page=2", "/de/places/map/?q=alps&page=2"):
            response = self.client.get(path)

            self.assertRedirects(response, "/de/places/search/?q=alps&page=2", fetch_redirect_response=False)


    def test_article_omits_an_intro_missing_from_the_selected_language(self):
        story = Page.objects.create(
            title_de="Deutscher Titel", title_ru="Русский заголовок", intro_ru="Русское вступление",
            page_type="story", slug="story", is_published=True,
        )
        body = RichTextBlock.objects.create(body_de="Deutscher Text")
        PageBlockSlot.objects.create(page=story, content_object=body)

        response = self.client.get("/de/story/")

        self.assertEqual(response.context["article_language"], "de")
        self.assertEqual(response.context["article_intro"], "")
        self.assertNotContains(response, "Русское вступление")

    def test_fallback_article_keeps_interface_copy_in_requested_locale(self):
        story = Page.objects.create(
            title_ru="Русский заголовок", page_type="story", slug="fallback-story", is_published=True
        )
        body = RichTextBlock.objects.create(body_ru="Русский текст")
        PageBlockSlot.objects.create(page=story, content_object=body)

        response = self.client.get("/de/fallback-story/")

        self.assertEqual(response.context["active_locale"], "de")
        self.assertEqual(response.context["article_language"], "ru")
        self.assertContains(response, "Startseite")
        self.assertContains(response, "Geschichten von Orten")
        self.assertContains(response, "Dieser Beitrag ist derzeit auf RU verfügbar.")
        self.assertContains(response, "Русский заголовок")
        self.assertContains(response, "Русский текст")

    def test_preview_recomputes_raw_title_intro_and_meta_for_selected_language(self):
        author = get_user_model().objects.create_superuser(
            username="preview-author", email="preview@example.test", password="test-password"
        )
        self.client.force_login(author)
        story = Page.objects.create(
            title_ru="Русский заголовок",
            title_de="Deutscher Titel",
            intro_ru="Русское вступление",
            intro_de="Deutsche Einführung",
            seo_title_ru="Русский SEO",
            seo_title_de="Deutscher SEO-Titel",
            seo_description_ru="Русское SEO-описание",
            seo_description_de="Deutsche SEO-Beschreibung",
            page_type="story",
            slug="preview-story",
        )
        body = RichTextBlock.objects.create(body_ru="Русский текст", body_de="Deutscher Text")
        PageBlockSlot.objects.create(page=story, content_object=body)

        response = self.client.get(reverse("cabinet:article_preview", args=[story.pk]), {"language": "de"})

        self.assertEqual(response.context["article_language"], "de")
        self.assertEqual(response.context["article_title"], "Deutscher Titel")
        self.assertEqual(response.context["article_intro"], "Deutsche Einführung")
        self.assertEqual(response.context["article_meta_title"], "Deutscher SEO-Titel")
        self.assertEqual(response.context["article_meta_description"], "Deutsche SEO-Beschreibung")
        self.assertContains(response, "Deutscher SEO-Titel")
        self.assertNotContains(response, "Русский SEO")

