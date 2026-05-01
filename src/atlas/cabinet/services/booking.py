
from typing import Any


class BookingService:
    """Fallback service when booking module is not installed."""

    @staticmethod
    def _disabled() -> dict[str, Any]:
        return {
            "ok": False,
            "code": "booking-disabled",
            "message": "Booking module is disabled in this scaffold.",
            "target_url": "#",
            "redirect_url": "#",
        }

    @classmethod
    def get_schedule_context(cls, request: Any) -> dict[str, Any]:
        return {}

    @classmethod
    def get_new_booking_context(cls, request: Any) -> dict[str, Any]:
        return {}

    @classmethod
    def get_list_context(cls, request: Any, status: str | None = None) -> dict[str, Any]:
        return {}

    @classmethod
    def create_new_booking(cls, request: Any) -> dict[str, Any]:
        return cls._disabled()

    @classmethod
    def get_booking_modal_context(cls, request: Any, booking_id: int) -> dict[str, Any]:
        return {}

    @classmethod
    def perform_action(cls, request: Any, booking_id: int, action: str) -> dict[str, Any]:
        return cls._disabled()
