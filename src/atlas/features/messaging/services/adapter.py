from codex_django.messaging import DjangoDirectAdapter
from django.core.mail import EmailMultiAlternatives
from system.models import EmailSettings


class AtlasMessagingDirectAdapter(DjangoDirectAdapter):
    def _resolve_from_email(self) -> str:
        settings = EmailSettings.load()
        email = settings.email_from.strip()
        if not email:
            return super()._resolve_from_email()
        name = settings.email_sender_name.strip()
        return f"{name} <{email}>" if name else email

    def _send(self, payload: dict[str, object]) -> str | None:
        mode = str(payload.get("mode", "rendered"))
        if mode == "template":
            html_content, text_content = self._render(payload)
        else:
            html_content = str(payload.get("html_content", ""))
            text_content = str(payload.get("text_content", ""))

        recipient = str(payload.get("recipient_email", "")).strip()
        if not recipient:
            return None

        settings = EmailSettings.load()
        message = EmailMultiAlternatives(
            subject=str(payload.get("subject", "")),
            body=text_content,
            from_email=self._resolve_from_email(),
            to=[recipient],
            reply_to=[settings.email_reply_to] if settings.email_reply_to else None,
        )
        if html_content:
            message.attach_alternative(html_content, "text/html")
        message.send(fail_silently=False)
        return None
