from django.test import TestCase
from system.models import EmailSettings, SiteSettings


class EmailSettingsTests(TestCase):
    def test_load_returns_singleton(self):
        settings_obj = EmailSettings.load()
        settings_obj.email_from = "hello@example.com"
        settings_obj.save()

        loaded_again = EmailSettings.load()

        self.assertEqual(settings_obj.pk, 1)
        self.assertEqual(loaded_again.pk, 1)
        self.assertEqual(loaded_again.email_from, "hello@example.com")

    def test_site_settings_no_longer_exposes_email_surface(self):
        field_names = {field.name for field in SiteSettings._meta.get_fields()}

        for removed_name in {
            "email_from",
            "email_sender_name",
            "email_reply_to",
            "site_base_url",
            "logo_url",
            "url_path_confirm",
            "url_path_cancel",
            "url_path_reschedule",
            "url_path_contact_form",
        }:
            self.assertNotIn(removed_name, field_names)
