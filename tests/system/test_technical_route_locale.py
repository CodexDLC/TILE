# ruff: noqa: S106
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class TechnicalRouteLocaleTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = get_user_model().objects.create_superuser(
            username="author", email="author@example.test", password="test-password"
        )

    def test_accounts_login_uses_accept_language(self):
        response = self.client.get("/accounts/login/", HTTP_ACCEPT_LANGUAGE="ru-RU,ru;q=0.9,en;q=0.8")

        self.assertContains(response, '<html lang="ru">')
        self.assertContains(response, "Войти")

    def test_cabinet_prefers_language_cookie_over_accept_language(self):
        self.client.force_login(self.author)
        self.client.cookies[settings.LANGUAGE_COOKIE_NAME] = "de"

        response = self.client.get(reverse("cabinet:article_create"), HTTP_ACCEPT_LANGUAGE="ru")

        self.assertContains(response, '<html lang="de">')
        self.assertContains(response, "Neuer Artikel")
        self.assertContains(response, "Artikeltitel")

    def test_public_prefixed_route_ignores_technical_route_cookie_override(self):
        self.client.cookies[settings.LANGUAGE_COOKIE_NAME] = "de"

        response = self.client.get("/ru/places/search/", HTTP_ACCEPT_LANGUAGE="en")

        self.assertContains(response, '<html lang="ru">')
        self.assertContains(response, "Найдите свою историю")

    def test_public_default_route_keeps_default_language_without_prefix(self):
        response = self.client.get("/places/search/", HTTP_ACCEPT_LANGUAGE="ru")

        self.assertContains(response, '<html lang="en">')
        self.assertContains(response, "Find your story")
