from importlib import import_module

from django.apps import apps as django_apps
from django.db import connection
from django.test import TestCase

from system.models import EmailSettings, SiteSettings


class MessagingMigrationTests(TestCase):
    def test_bootstrap_copies_legacy_site_settings_into_email_settings(self):
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
