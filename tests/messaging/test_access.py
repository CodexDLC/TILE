from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.test import RequestFactory, TestCase
from django.urls import reverse
from features.messaging.models import Message, MessageReply, Thread
from features.messaging.views import cabinet
from system.models import EmailSettings


class MessagingStaffAccessTests(TestCase):
    list_routes = (
        "cabinet:messaging_inbox",
        "cabinet:messaging_campaigns",
        "cabinet:messaging_recipients",
        "cabinet:messaging_delivery_log",
        "cabinet:messaging_settings",
    )

    def setUp(self):
        self.member = get_user_model().objects.create_user(username="member")
        self.editor = get_user_model().objects.create_user(username="editor", is_staff=True)
        self.owner = get_user_model().objects.create_user(username="owner", is_superuser=True)
        self.thread = Thread.objects.create(sender_email="reader@example.test", subject="Private inquiry")
        self.settings = EmailSettings.load()
        self.settings.email_sender_name = "Original sender"
        self.settings.save()

    def test_anonymous_mailbox_routes_require_login(self):
        routes = [reverse(name) for name in self.list_routes]
        routes.append(reverse("cabinet:messaging_detail", args=[self.thread.pk]))
        routes.append(reverse("cabinet:messaging_thread_action", args=[self.thread.pk, "archive"]))
        for url in routes:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 302)
                self.assertIn("/login/", response.url)
        self.thread.refresh_from_db()
        self.assertFalse(self.thread.is_read)

    def test_member_cannot_read_global_messaging_data(self):
        self.client.force_login(self.member)
        with patch("features.messaging.views.cabinet._bridge", wraps=cabinet._bridge) as bridge:
            for name in self.list_routes:
                with self.subTest(route=name):
                    self.assertEqual(self.client.get(reverse(name)).status_code, 403)
            bridge.assert_not_called()

    def test_member_cannot_mark_read_or_reply_archive_and_change_settings(self):
        self.client.force_login(self.member)
        with self.subTest(action="detail"):
            response = self.client.get(reverse("cabinet:messaging_detail", args=[self.thread.pk]))
            self.assertEqual(response.status_code, 403)
        for action in ("reply", "mark_processed", "mark_spam", "archive"):
            with self.subTest(action=action):
                with patch("features.messaging.services.workflow.notify_thread_reply"):
                    response = self.client.post(
                        reverse("cabinet:messaging_thread_action", args=[self.thread.pk, action]),
                        {"body": "Unauthorized reply"},
                    )
                self.assertEqual(response.status_code, 403)
        with self.subTest(action="settings"):
            response = self.client.post(reverse("cabinet:messaging_settings"), {"email_sender_name": "Changed"})
            self.assertEqual(response.status_code, 403)
        self.thread.refresh_from_db()
        self.settings.refresh_from_db()
        self.assertFalse(self.thread.is_read)
        self.assertFalse(self.thread.is_archived)
        self.assertEqual(self.thread.status, Thread.Status.OPEN)
        self.assertEqual(Message.objects.count(), 0)
        self.assertEqual(MessageReply.objects.count(), 0)
        self.assertEqual(self.settings.email_sender_name, "Original sender")

    def test_active_editor_and_superuser_keep_read_and_write_access(self):
        for user in (self.editor, self.owner):
            self.thread.is_archived = False
            self.thread.is_read = False
            self.thread.save(update_fields=["is_archived", "is_read"])
            self.client.force_login(user)
            for name in self.list_routes:
                with self.subTest(user=user.username, route=name):
                    response = self.client.get(reverse(name))
                    self.assertEqual(response.status_code, 200)
                    self.assertEqual(response.wsgi_request.cabinet_space, "staff")
            response = self.client.get(reverse("cabinet:messaging_detail", args=[self.thread.pk]))
            self.assertEqual(response.status_code, 200)
            self.thread.refresh_from_db()
            self.assertTrue(self.thread.is_read)
            response = self.client.post(
                reverse("cabinet:messaging_thread_action", args=[self.thread.pk, "archive"])
            )
            self.assertEqual(response.status_code, 302)
            self.thread.refresh_from_db()
            self.assertTrue(self.thread.is_archived)
            response = self.client.post(
                reverse("cabinet:messaging_settings"), {"email_sender_name": user.username}
            )
            self.assertEqual(response.status_code, 302)
            self.settings.refresh_from_db()
            self.assertEqual(self.settings.email_sender_name, user.username)

    def test_inactive_staff_and_superuser_are_denied_before_bridge(self):
        factory = RequestFactory()
        views = (
            (cabinet.inbox_view, {}),
            (cabinet.detail_view, {"pk": self.thread.pk}),
            (cabinet.thread_action_view, {"pk": self.thread.pk, "action": "archive"}),
            (cabinet.campaigns_view, {}),
            (cabinet.recipients_view, {}),
            (cabinet.delivery_log_view, {}),
            (cabinet.settings_view, {}),
        )
        with patch("features.messaging.views.cabinet._bridge") as bridge:
            for user in (self.editor, self.owner):
                user.is_active = False
                for view, kwargs in views:
                    request = factory.post("/cabinet/messaging/", {"body": "Unauthorized reply"})
                    request.user = user
                    with self.subTest(user=user.username, view=view), self.assertRaises(PermissionDenied):
                        view(request, **kwargs)
            bridge.assert_not_called()
