from django.test import TestCase, override_settings

from codex_django.messaging import messaging_event_registry

from features.messaging.models import Message, Thread
from features.messaging.services import create_reply


class MessagingRegistryTests(TestCase):
    def setUp(self):
        self.thread = Thread.objects.create(
            sender_name="Alice",
            sender_email="alice@example.com",
            subject="Need help",
            topic="support",
            source="contact_form",
            channel="email",
        )
        self.message = Message.objects.create(
            thread=self.thread,
            direction=Message.Direction.INBOUND,
            sender_name="Alice",
            sender_email="alice@example.com",
            subject="Need help",
            body="Please call me back.",
            source="contact_form",
            channel="email",
        )

    @override_settings(ADMINS=(("Ops", "ops@example.com"),))
    def test_new_message_handler_returns_shared_registry_specs(self):
        specs = messaging_event_registry.build_specs("messaging.new_message", self.thread)

        self.assertEqual(len(specs), 1)
        self.assertEqual(specs[0].recipient_email, "ops@example.com")
        self.assertEqual(specs[0].mode, "rendered")
        self.assertEqual(specs[0].event_type, "messaging.new_message")

    def test_thread_reply_handler_returns_rendered_spec(self):
        reply = create_reply(thread=self.thread, body="We are on it.", user=None)

        specs = messaging_event_registry.build_specs("messaging.thread_reply", self.thread, reply)

        self.assertEqual(len(specs), 1)
        self.assertEqual(specs[0].recipient_email, "alice@example.com")
        self.assertEqual(specs[0].mode, "rendered")
        self.assertIn("We are on it.", specs[0].text_content)
