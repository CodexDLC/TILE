import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


def bootstrap_email_settings_and_migrate_data(apps, schema_editor):
    from system.models import EmailSettings

    existing_tables = set(schema_editor.connection.introspection.table_names())
    if EmailSettings._meta.db_table not in existing_tables:
        schema_editor.create_model(EmailSettings)

    email_settings = EmailSettings.objects.filter(pk=1).first() or EmailSettings(pk=1)
    legacy_field_names = (
        "email_from",
        "email_sender_name",
        "email_reply_to",
        "site_base_url",
        "logo_url",
        "url_path_confirm",
        "url_path_cancel",
        "url_path_reschedule",
        "url_path_contact_form",
    )
    if "system_sitesettings" in existing_tables:
        with schema_editor.connection.cursor() as cursor:
            description = schema_editor.connection.introspection.get_table_description(cursor, "system_sitesettings")
            available_columns = {column.name for column in description}
            selected_columns = [field_name for field_name in legacy_field_names if field_name in available_columns]
            if selected_columns:
                sql = f"SELECT {', '.join(selected_columns)} FROM system_sitesettings WHERE id = 1"
                cursor.execute(sql)
                row = cursor.fetchone()
                if row is not None:
                    for field_name, value in zip(selected_columns, row, strict=False):
                        setattr(email_settings, field_name, value or "")
    email_settings.save()


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("system", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Campaign",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("subject", models.CharField(max_length=255)),
                ("body_text", models.TextField(blank=True)),
                ("template_key", models.CharField(blank=True, max_length=128)),
                ("locale", models.CharField(default="de", max_length=8)),
                ("body_translations", models.JSONField(blank=True, default=dict)),
                ("audience_filter", models.JSONField(default=dict)),
                ("status", models.CharField(default="draft", max_length=16)),
                ("send_at", models.DateTimeField(blank=True, null=True)),
                ("sent_at", models.DateTimeField(blank=True, null=True)),
                ("arq_parent_job_id", models.CharField(blank=True, max_length=128)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="EmailLog",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("notification_id", models.CharField(db_index=True, max_length=128, unique=True)),
                ("event_type", models.CharField(db_index=True, max_length=128)),
                ("channel", models.CharField(max_length=32)),
                ("recipient", models.CharField(max_length=255)),
                ("status", models.CharField(db_index=True, max_length=16)),
                ("subject", models.CharField(blank=True, max_length=255)),
                ("error_message", models.TextField(blank=True)),
                ("context_preview", models.JSONField(blank=True, null=True)),
                ("provider_message_id", models.CharField(blank=True, max_length=128)),
                ("message_id_header", models.CharField(blank=True, max_length=255)),
                ("queued_at", models.DateTimeField(auto_now_add=True)),
                ("sent_at", models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="SystemRecipient",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("kind", models.CharField(max_length=32)),
                ("enabled", models.BooleanField(default=True)),
                ("note", models.CharField(blank=True, max_length=255)),
                ("name", models.CharField(blank=True, max_length=128)),
                ("locale", models.CharField(default="de", max_length=8)),
                ("unsubscribe_token", models.CharField(blank=True, max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name="Thread",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("thread_key", models.CharField(db_index=True, max_length=64, unique=True)),
                ("subject", models.CharField(blank=True, max_length=255)),
                ("status", models.CharField(default="open", max_length=16)),
                ("last_activity_at", models.DateTimeField(auto_now=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("topic", models.CharField(blank=True, db_index=True, max_length=30)),
                ("source", models.CharField(blank=True, db_index=True, max_length=20)),
                ("channel", models.CharField(db_index=True, default="email", max_length=20)),
                ("sender_name", models.CharField(blank=True, max_length=255)),
                ("sender_email", models.EmailField(blank=True, max_length=254)),
                ("sender_phone", models.CharField(blank=True, max_length=50)),
                ("is_read", models.BooleanField(db_index=True, default=False)),
                ("is_archived", models.BooleanField(db_index=True, default=False)),
            ],
            options={"ordering": ["-last_activity_at"]},
        ),
        migrations.CreateModel(
            name="Message",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("direction", models.CharField(max_length=16)),
                ("sender_name", models.CharField(blank=True, max_length=128)),
                ("sender_email", models.EmailField(max_length=254)),
                ("recipient_email", models.EmailField(blank=True, max_length=254)),
                ("subject", models.CharField(blank=True, max_length=255)),
                ("body", models.TextField()),
                ("source", models.CharField(max_length=32)),
                ("channel", models.CharField(default="email", max_length=32)),
                ("message_id_header", models.CharField(blank=True, db_index=True, max_length=255)),
                ("in_reply_to_header", models.CharField(blank=True, max_length=255)),
                ("references_header", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "thread",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="messages", to="messaging.thread"
                    ),
                ),
            ],
            options={"ordering": ["created_at"]},
        ),
        migrations.CreateModel(
            name="MessageReply",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("body", models.TextField()),
                ("is_inbound", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("sent_at", models.DateTimeField(auto_now_add=True)),
                (
                    "message",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="replies",
                        to="messaging.message",
                        verbose_name="message",
                    ),
                ),
                (
                    "sent_by",
                    models.ForeignKey(
                        null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
            options={"ordering": ["sent_at"]},
        ),
        migrations.CreateModel(
            name="CampaignRecipient",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("recipient_id", models.CharField(db_index=True, max_length=64)),
                ("email", models.EmailField(max_length=254)),
                ("first_name", models.CharField(blank=True, max_length=128)),
                ("last_name", models.CharField(blank=True, max_length=128)),
                ("locale", models.CharField(default="de", max_length=8)),
                ("status", models.CharField(db_index=True, default="queued", max_length=16)),
                ("notification_id", models.CharField(blank=True, db_index=True, max_length=128)),
                ("error_message", models.TextField(blank=True)),
                ("provider_message_id", models.CharField(blank=True, max_length=128)),
                ("unsubscribe_token", models.CharField(blank=True, max_length=128)),
                ("arq_job_id", models.CharField(blank=True, max_length=128)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "campaign",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="recipients", to="messaging.campaign"
                    ),
                ),
            ],
        ),
        migrations.RunPython(bootstrap_email_settings_and_migrate_data, migrations.RunPython.noop),
    ]
