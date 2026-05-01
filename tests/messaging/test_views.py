from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from features.messaging.models import Thread
from system.models import EmailSettings


class MessagingViewsTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.create_user(username="staff", password="secret", is_staff=True)
        self.client.force_login(self.user)

    def test_cabinet_routes_render(self):
        Thread.objects.create(
            sender_name="Alice",
            sender_email="alice@example.com",
            subject="Hello",
            topic="general",
            source="contact_form",
            channel="email",
        )

        for url_name in (
            "cabinet:messaging_inbox",
            "cabinet:messaging_templates",
            "cabinet:messaging_log",
            "cabinet:messaging_settings",
        ):
            response = self.client.get(reverse(url_name))
            self.assertEqual(response.status_code, 200, url_name)

    def test_messaging_settings_view_persists_values(self):
        response = self.client.post(
            reverse("cabinet:messaging_settings"),
            {
                "email_from": "ops@example.com",
                "email_sender_name": "Atlas",
                "email_reply_to": "reply@example.com",
                "site_base_url": "https://atlas.example.com",
                "logo_url": "/logo.svg",
                "url_path_confirm": "/confirm/",
                "url_path_cancel": "/cancel/",
                "url_path_reschedule": "/reschedule/",
                "url_path_contact_form": "/contact/",
            },
        )

        self.assertEqual(response.status_code, 302)
        settings_obj = EmailSettings.load()
        self.assertEqual(settings_obj.email_from, "ops@example.com")
        self.assertEqual(settings_obj.url_path_contact_form, "/contact/")
