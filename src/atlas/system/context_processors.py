from typing import Any

from django.http import HttpRequest

from .models import EmailSettings


def email_settings(request: HttpRequest) -> dict[str, Any]:
    return {"email_settings": EmailSettings.load()}
