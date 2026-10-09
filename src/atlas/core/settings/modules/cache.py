import os
from pathlib import Path
from urllib.parse import quote_plus, urlparse

# In container: /app. Locally: src/backend_django
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
PROJECT_NAME = BASE_DIR.name

# ═══════════════════════════════════════════
# Redis & ARQ
# ═══════════════════════════════════════════

REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", None)
REDIS_URL = os.environ.get("REDIS_URL", "").strip()
ARQ_REDIS_URL = os.environ.get("ARQ_REDIS_URL", "").strip()

UPSTASH_REDIS_REST_URL = os.environ.get("UPSTASH_REDIS_REST_URL", "").strip()
UPSTASH_REDIS_HOST = os.environ.get("UPSTASH_REDIS_HOST", "").strip()
UPSTASH_REDIS_PASSWORD = os.environ.get("UPSTASH_REDIS_PASSWORD", "").strip()

if not UPSTASH_REDIS_HOST and UPSTASH_REDIS_REST_URL:
    UPSTASH_REDIS_HOST = urlparse(UPSTASH_REDIS_REST_URL).hostname or ""

IS_INSIDE_DOCKER = os.path.exists("/.dockerenv")
if REDIS_HOST == "localhost" and IS_INSIDE_DOCKER:
    REDIS_HOST = "redis"

if not REDIS_URL and UPSTASH_REDIS_HOST and UPSTASH_REDIS_PASSWORD:
    encoded_password = quote_plus(UPSTASH_REDIS_PASSWORD.strip("'\"").strip())
    REDIS_URL = f"rediss://default:{encoded_password}@{UPSTASH_REDIS_HOST}:6379/0"
elif not REDIS_URL and REDIS_PASSWORD:
    clean_password = REDIS_PASSWORD.strip("'\"").strip()
    encoded_password = quote_plus(clean_password)
    REDIS_URL = f"redis://:{encoded_password}@{REDIS_HOST}:{REDIS_PORT}/0"
elif not REDIS_URL:
    REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"

if not ARQ_REDIS_URL:
    ARQ_REDIS_URL = REDIS_URL

# ═══════════════════════════════════════════
# Cache & Sessions (Isolated by PROJECT_NAME)
# ═══════════════════════════════════════════

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "KEY_PREFIX": PROJECT_NAME,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
SESSION_COOKIE_NAME = f"sessionid_{PROJECT_NAME}"

# --- Ratelimit ---
RATELIMIT_USE_CACHE = "default"
RATELIMIT_VIEW = "features.main.views.legal.ratelimit_view"
