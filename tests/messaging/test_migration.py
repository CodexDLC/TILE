from importlib import import_module

from django.db import connection
from django.apps import apps as django_apps
from django.test import TestCase

from features.conversations.models import Message as LegacyMessage
from features.conversations.models import MessageReply as LegacyMessageReply
from features.messaging.models import Message, MessageReply, Thread
from system.models import EmailSettings, SiteSettings


class MessagingMigrationTests(TestCase):
    def test_bootstrap_copies_site_settings_and_conversation_rows(self):
        site_settings = SiteSettings.load()
        site_settings.email = "contact@example.com"
        site_settings.save()
        with connection.cursor() as cursor:
            for field_name in (
                "email_from",
                "email_sender_name",
                "email_reply_to",
                "site_base_url",
                "logo_url",
                "url_path_confirm",
                "url_path_cancel",
                "url_path_reschedule",
                "url_path_contact_form",
            ):
                cursor.execute(f"ALTER TABLE system_sitesettings ADD COLUMN {field_name} varchar(255)")
            cursor.execute(
                """
                UPDATE system_sitesettings
                SET email_from = %s,
                    email_sender_name = %s,
                    email_reply_to = %s,
                    site_base_url = %s,
                    logo_url = %s,
                    url_path_confirm = %s,
                    url_path_cancel = %s,
                    url_path_reschedule = %s,
                    url_path_contact_form = %s
                WHERE id = 1
                """,
                [
                    "from@example.com",
                    "Atlas",
                    "reply@example.com",
                    "https://atlas.example.com",
                    "/logo.svg",
                    "/confirm/",
                    "/cancel/",
                    "/reschedule/",
                    "/contact/",
                ],
            )

        legacy_message = LegacyMessage.objects.create(
            sender_name="Alice",
            sender_email="alice@example.com",
            sender_phone="+49123",
            subject="Booking",
            body="I need a booking slot.",
            topic=LegacyMessage.Topic.BOOKING,
            source=LegacyMessage.Source.CONTACT_FORM,
            channel=LegacyMessage.Channel.EMAIL,
            status=LegacyMessage.Status.OPEN,
            is_read=False,
            is_archived=False,
        )
        LegacyMessageReply.objects.create(message=legacy_message, body="Thanks", is_inbound=False)

        Thread.objects.all().delete()
        Message.objects.all().delete()
        MessageReply.objects.all().delete()
        EmailSettings.objects.all().delete()

        migration_module = import_module("features.messaging.migrations.0001_initial")
        schema_editor = type(
            "SchemaEditorStub",
            (),
            {"connection": connection, "create_model": staticmethod(lambda model: None)},
        )()
        migration_module.bootstrap_email_settings_and_migrate_data(django_apps, schema_editor)

        email_settings = EmailSettings.load()
        self.assertEqual(email_settings.email_from, "from@example.com")
        self.assertEqual(email_settings.logo_url, "/logo.svg")

        thread = Thread.objects.get(pk=legacy_message.pk)
        root_message = Message.objects.get(pk=legacy_message.pk)
        replies = MessageReply.objects.filter(message=root_message)

        self.assertEqual(thread.thread_key, legacy_message.thread_key)
        self.assertEqual(root_message.body, "I need a booking slot.")
        self.assertEqual(replies.count(), 1)
