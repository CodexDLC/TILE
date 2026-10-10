from unittest.mock import patch

from codex_django.cabinet import context_processors as library_context
from codex_django.cabinet.views.site_settings import site_settings_view
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import resolve


class CabinetLibraryIntegrationTests(TestCase):
    def test_shell_uses_library_context_processors(self):
        processors = settings.TEMPLATES[0]["OPTIONS"]["context_processors"]
        self.assertIn(f"{library_context.__name__}.cabinet", processors)
        self.assertIn(f"{library_context.__name__}.notifications", processors)
        self.assertNotIn("cabinet.context_processors.cabinet", processors)

    def test_settings_route_uses_library_view(self):
        self.assertIs(resolve("/cabinet/site/settings/").func, site_settings_view)

    def test_regular_user_cannot_read_or_save_site_settings(self):
        user = get_user_model().objects.create_user(username="reader")
        self.client.force_login(user)
        with patch("system.services.site_settings.SiteSettingsService.save_context") as save:
            for method in (self.client.get, self.client.post):
                response = method("/cabinet/site/settings/")
                self.assertEqual(response.status_code, 403)
            save.assert_not_called()

    def test_staff_can_open_settings_with_library_extension(self):
        user = get_user_model().objects.create_user(username="editor", is_staff=True)
        self.client.force_login(user)
        response = self.client.get("/cabinet/site/settings/")
        self.assertEqual(response.status_code, 200)

    def test_client_home_requires_login(self):
        response = self.client.get("/cabinet/my/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/cabinet/login/", response.url)

    def test_client_home_renders_without_unimplemented_navigation(self):
        user = get_user_model().objects.create_user(username="client")
        self.client.force_login(user)
        response = self.client.get("/cabinet/my/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["cabinet_space"], "client")
        self.assertIsNone(response.context["cabinet_settings_url"])
