from typing import Any

from django.core.exceptions import PermissionDenied


def require_staff(user: Any) -> None:
    """Apply the cabinet's active staff-or-superuser policy to function views."""
    if not (
        getattr(user, "is_authenticated", False)
        and getattr(user, "is_active", False)
        and (getattr(user, "is_staff", False) or getattr(user, "is_superuser", False))
    ):
        raise PermissionDenied
