
from dataclasses import dataclass
from typing import Any


@dataclass
class ConversationsService:
    """Fallback service when conversations module is not installed."""

    @staticmethod
    def get_inbox_context(request: Any, *, default_folder: str = "open") -> dict[str, Any]:
        return {}

    @staticmethod
    def get_thread_context(*, pk: int) -> dict[str, Any]:
        return {}

    @staticmethod
    def reply_to_thread(*, pk: int, body: str, user: object) -> dict[str, Any]:
        return _disabled_result()

    @staticmethod
    def perform_thread_action(*, pk: int, action: str) -> dict[str, Any]:
        return _disabled_result()

    @staticmethod
    def compose_message(*, request: Any) -> dict[str, Any]:
        return _disabled_result()

    @staticmethod
    def perform_bulk_action(*, request: Any) -> dict[str, Any]:
        return _disabled_result()

    @staticmethod
    def check_inbox() -> dict[str, Any]:
        return _disabled_result()


def _disabled_result() -> dict[str, Any]:
    return {
        "ok": False,
        "code": "conversations-disabled",
        "message": "Conversations module is disabled in this scaffold.",
        "redirect_url": "#",
        "meta": {},
    }
