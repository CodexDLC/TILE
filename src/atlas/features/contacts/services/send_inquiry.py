from django.conf import settings
from django.core.mail import send_mail
from system.models import SiteSettings


def send_inquiry(*, name: str, email: str, topic: str, message: str) -> None:
    site_settings = SiteSettings.load()
    recipient = site_settings.email or getattr(settings, "DEFAULT_FROM_EMAIL", "")
    if not recipient:
        return

    subject = topic or "Atlas contact inquiry"
    body = f"Name: {name}\nEmail: {email}\n\n{message}"
    send_mail(
        subject=subject,
        message=body,
        from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
        recipient_list=[recipient],
        fail_silently=False,
    )
