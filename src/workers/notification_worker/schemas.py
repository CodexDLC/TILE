from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator


class RecipientSchema(BaseModel):
    email: str | None = None
    phone: str | None = None
    first_name: str = ""
    last_name: str = ""


class NotificationPayload(BaseModel):
    notification_id: str = ""
    recipient: RecipientSchema = Field(default_factory=RecipientSchema)

    recipient_email: str | None = None
    recipient_phone: str | None = None
    client_name: str | None = None

    template_name: str | None = None
    subject: str = ""
    mode: str = "rendered"
    html_content: str | None = None
    text_content: str | None = None
    event_type: str | None = None
    channels: list[str] = Field(default_factory=lambda: ["email"])
    context_data: dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(extra="ignore")

    @model_validator(mode="before")
    @classmethod
    def bridge_flat_to_recipient(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        if not data.get("recipient") and (
            data.get("recipient_email") or data.get("recipient_phone") or data.get("client_name")
        ):
            first_name = ""
            last_name = ""
            client_name = str(data.get("client_name") or "").strip()
            if client_name:
                parts = client_name.split(maxsplit=1)
                first_name = parts[0]
                last_name = parts[1] if len(parts) > 1 else ""
            data["recipient"] = {
                "email": data.get("recipient_email"),
                "phone": data.get("recipient_phone"),
                "first_name": first_name,
                "last_name": last_name,
            }

        return data
