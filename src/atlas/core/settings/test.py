"""
Test settings — used only for pytest.

Inherits from base settings but uses SQLite in-memory for speed.
"""

from .base import *  # noqa: F403

# Enable debug mode in tests for detailed error pages
DEBUG = True

# SQLite in-memory database for fast tests
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# In-memory cache for tests (no Redis)
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "test-cache",
    }
}

# Do not inherit external Redis/queue connections from the project .env.
CODEX_REDIS_ENABLED = False
REDIS_URL = ""
ARQ_REDIS_URL = ""
REDIS_PASSWORD = None
UPSTASH_REDIS_REST_URL = ""
UPSTASH_REDIS_HOST = ""
UPSTASH_REDIS_PASSWORD = ""

# Email backend for tests
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# Disable migrations for speed (optional)
# MIGRATION_MODULES = {app: None for app in INSTALLED_APPS}

# Fast password hasher for tests
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

# Keep test output in pytest; do not share rotating files with the dev server.
LOGURU_ENABLED = False
