from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase


class DisabledSmartCreateTests(TestCase):
    def test_create_page_uses_manual_form(self):
        user = get_user_model().objects.create_user(username="owner", is_staff=True, is_superuser=True)
        self.client.force_login(user)
        response = self.client.get("/cabinet/resources/content.page/create/")
        self.assertTemplateUsed(response, "cabinet/resources/form.html")

    def test_direct_preview_request_cannot_enqueue_translation(self):
        user = get_user_model().objects.create_user(username="owner", is_staff=True, is_superuser=True)
        self.client.force_login(user)
        with patch("features.content.services.smart_create.arq_client.enqueue", return_value="test-job") as enqueue:
            response = self.client.post(
                "/cabinet/resources/content.page/smart-preview/",
                data={"title": "Test", "page_type": "static"},
                content_type="application/json",
            )
            self.assertEqual(response.status_code, 403)
            enqueue.assert_not_called()
