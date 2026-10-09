# ruff: noqa: S106
from django.contrib.auth import get_user_model
from django.test import TestCase


class CabinetLoginTests(TestCase):
    def test_cabinet_login_form_posts_to_its_own_username_authentication_view(self):
        user = get_user_model().objects.create_user(username="editor", password="test-password")
        next_url = "/cabinet/articles/new/"

        response = self.client.get(f"/cabinet/login/?next={next_url}")

        self.assertContains(response, 'action="/cabinet/login/"')
        response = self.client.post(
            "/cabinet/login/",
            {"username": user.username, "password": "test-password", "next": next_url},
        )

        self.assertRedirects(response, next_url, fetch_redirect_response=False)

    def test_shared_login_override_keeps_brand_styling_and_next_for_allauth(self):
        next_url = "/cabinet/articles/"

        response = self.client.get(f"/accounts/login/?next={next_url}")

        self.assertContains(response, 'class="cab-auth__card"')
        self.assertContains(response, "TALE")
        self.assertContains(response, 'action="/accounts/login/"')
        self.assertContains(response, f'name="next" value="{next_url}"')

    def test_password_value_is_never_echoed_after_invalid_login(self):
        response = self.client.post(
            "/cabinet/login/",
            {"username": "unknown", "password": "do-not-echo-this"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "do-not-echo-this")

    def test_allauth_remember_checkbox_keeps_checked_state_after_error(self):
        response = self.client.post(
            "/accounts/login/",
            {"login": "unknown@example.test", "password": "wrong-password", "remember": "1"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="remember"')
        self.assertContains(response, 'value="1" checked')

