from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from features.messaging.models import Message, Thread


class PublicContactTests(TestCase):
    def test_form_renders_for_anonymous_visitor(self):
        response = self.client.get(reverse("messaging:contact"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="sender_email"')
        self.assertContains(response, 'name="body"')
        self.assertContains(response, 'name="csrfmiddlewaretoken"')

    def test_invalid_submission_preserves_input_and_does_not_create_thread(self):
        response = self.client.post(reverse("messaging:contact"), {"sender_email": "not-an-email", "body": "Hello"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("sender_email", response.context["form"].errors)
        self.assertContains(response, "Hello")
        self.assertFalse(Thread.objects.exists())

    @patch("features.messaging.views.contact.notify_new_message")
    def test_submission_creates_message_and_shows_confirmation(self, notify):
        response = self.client.post(
            reverse("messaging:contact"),
            {"sender_name": "Alice", "sender_email": "alice@example.com", "subject": "Visit", "body": "Hello"},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        thread = Thread.objects.get()
        self.assertEqual(Message.objects.get(thread=thread).body, "Hello")
        notify.assert_called_once_with(thread)
        self.assertContains(response, "Your message has been sent.")
