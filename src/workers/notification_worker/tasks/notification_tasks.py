from typing import Any

from arq import Retry
from codex_platform.notifications.clients.smtp import AsyncEmailClient
from loguru import logger as log

from workers.notification_worker.schemas import NotificationPayload


def _build_email_client(ctx: dict[str, Any]) -> AsyncEmailClient:
    settings = ctx["settings"]
    return AsyncEmailClient(
        smtp_host=settings.SMTP_HOST,
        smtp_port=settings.SMTP_PORT,
        smtp_user=settings.SMTP_USER,
        smtp_password=settings.SMTP_PASSWORD,
        smtp_from_email=settings.SMTP_FROM_EMAIL,
        smtp_use_tls=settings.SMTP_USE_TLS,
    )


async def send_universal_notification_task(
    ctx: dict[str, Any],
    payload: dict[str, Any] | None = None,
    payload_dict: dict[str, Any] | None = None,
) -> None:
    raw_payload = payload if payload is not None else payload_dict
    if raw_payload is None:
        log.error("NotificationWorker | missing payload")
        return

    try:
        payload_model = NotificationPayload(**raw_payload)
    except Exception as exc:
        log.error(f"NotificationWorker | invalid payload | error={exc}")
        return

    if "email" not in payload_model.channels:
        log.debug(f"NotificationWorker | no email channel | notification_id={payload_model.notification_id}")
        return

    recipient_email = payload_model.recipient.email
    if not recipient_email:
        log.warning(f"NotificationWorker | missing recipient email | notification_id={payload_model.notification_id}")
        return

    if payload_model.mode != "rendered" or not payload_model.html_content:
        log.warning(
            f"NotificationWorker | template payload skipped until worker templates are added | "
            f"notification_id={payload_model.notification_id}"
        )
        return

    client = _build_email_client(ctx)
    try:
        await client.send(
            to=recipient_email,
            subject=payload_model.subject,
            html_content=payload_model.html_content,
            text_content=payload_model.text_content,
        )
        log.info(f"NotificationWorker | sent | notification_id={payload_model.notification_id} | to={recipient_email}")
    except Exception as exc:
        log.error(f"NotificationWorker | send failed | notification_id={payload_model.notification_id} | error={exc}")
        raise Retry(defer=int(ctx.get("job_try", 1)) * 30) from exc


async def send_rendered_notification_task(ctx: dict[str, Any], payload: dict[str, Any]) -> None:
    await send_universal_notification_task(
        ctx,
        payload={
            "notification_id": str(payload.get("notification_id", "")),
            "recipient_email": payload.get("email") or payload.get("recipient_email"),
            "subject": payload.get("subject", ""),
            "html_content": payload.get("html_content"),
            "text_content": payload.get("text_content"),
            "mode": "rendered",
            "channels": ["email"],
        },
    )
