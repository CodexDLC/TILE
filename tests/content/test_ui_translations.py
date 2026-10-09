# ruff: noqa: RUF001, S106
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext, override
from features.content.models import Page
from features.places.models import City, Country, Region


class UiTranslationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.country_page = Page.objects.create(
            title_en="Germany",
            title_de="Deutschland",
            title_ru="Германия",
            intro_en="Country introduction",
            intro_de="Ländereinführung",
            intro_ru="Вступление о стране",
            page_type=Page.PageType.COUNTRY,
            slug="germany",
            is_published=True,
        )
        cls.country = Country.objects.create(
            page=cls.country_page,
            slug="germany",
            name_en="Germany",
            name_de="Deutschland",
            name_ru="Германия",
        )
        cls.region_page = Page.objects.create(
            parent=cls.country_page,
            title_en="Bavaria",
            title_de="Bayern",
            title_ru="Бавария",
            intro_en="Region introduction",
            intro_de="Regionseinführung",
            intro_ru="Вступление о регионе",
            page_type=Page.PageType.REGION,
            slug="bavaria",
            is_published=True,
        )
        cls.region = Region.objects.create(
            country=cls.country,
            page=cls.region_page,
            slug="bavaria",
            name_en="Bavaria",
            name_de="Bayern",
            name_ru="Бавария",
        )
        cls.city_page = Page.objects.create(
            parent=cls.region_page,
            title_en="Munich",
            title_de="München",
            title_ru="Мюнхен",
            page_type=Page.PageType.CITY,
            slug="munich",
            is_published=True,
        )
        City.objects.create(
            region=cls.region,
            page=cls.city_page,
            slug="munich",
            name_en="Munich",
            name_de="München",
            name_ru="Мюнхен",
        )
        cls.author = get_user_model().objects.create_superuser(
            username="author", email="author@example.test", password="test-password"
        )

    def test_country_and_region_render_without_hero_in_all_interface_languages(self):
        expectations = {
            "en": ("Editor note", "The regions", "Cities", "Places", "Start with Bavaria"),
            "de": ("Redaktioneller Hinweis", "Die Regionen", "Städte", "Orte", "Beginnen Sie mit Bayern"),
            "ru": ("Заметка редакции", "Регионы", "Города", "Места", "Начните с Бавария"),
        }
        for language, labels in expectations.items():
            prefix = "" if language == "en" else f"/{language}"
            with self.subTest(language=language, page="country"):
                response = self.client.get(f"{prefix}/germany/")
                self.assertEqual(response.status_code, 200)
                for label in labels[:4]:
                    self.assertContains(response, label)
            with self.subTest(language=language, page="region"):
                response = self.client.get(f"{prefix}/germany/bavaria/")
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, labels[0])
                self.assertContains(response, labels[4])

    def test_search_route_uses_gettext_in_all_interface_languages(self):
        expectations = {
            "en": ("Find your story", "City, place or story", "Search"),
            "de": ("Finden Sie Ihre Geschichte", "Stadt, Ort oder Geschichte", "Suchen"),
            "ru": ("Найдите свою историю", "Город, место или история", "Поиск"),
        }
        for language, labels in expectations.items():
            prefix = "" if language == "en" else f"/{language}"
            response = self.client.get(f"{prefix}/places/search/")
            self.assertEqual(response.status_code, 200)
            for label in labels:
                self.assertContains(response, label)

    def test_article_list_and_form_have_localized_workflow_copy(self):
        self.client.force_login(self.author)
        list_response = self.client.get(reverse("cabinet:article_list"))
        self.assertContains(list_response, "Articles")
        self.assertContains(list_response, "Create article")
        form_response = self.client.get(reverse("cabinet:article_create"))
        self.assertContains(form_response, "New article")
        self.assertContains(form_response, "Article title")

        for language, labels in {
            "de": ("Artikel", "Artikel erstellen", "Neuer Artikel", "Artikeltitel"),
            "ru": ("Статьи", "Создать статью", "Новая статья", "Заголовок статьи"),
        }.items():
            with override(language):
                self.assertEqual(gettext("Articles"), labels[0])
                self.assertEqual(gettext("Create article"), labels[1])
                self.assertEqual(gettext("New article"), labels[2])
                self.assertEqual(gettext("Article title"), labels[3])
