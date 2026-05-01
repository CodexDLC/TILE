"""Compatibility wrapper for booking bridge access inside the sandbox cabinet."""
__all__: list[str] = []


def get_booking_bridge() -> None:
    raise RuntimeError("Booking module is not installed in this scaffold.")
