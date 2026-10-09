import os
from pathlib import Path

# Root of Django project: src/backend_django
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

# ═══════════════════════════════════════════
# Internationalization
# ═══════════════════════════════════════════

LANGUAGE_CODE = os.environ.get("LANGUAGE_CODE", "en")
LANGUAGES = [
    ("en", "English"),
    ("de", "Deutsch"),
    ("ru", "Русский"),
]
MODELTRANSLATION_DEFAULT_LANGUAGE = "en"
MODELTRANSLATION_LANGUAGES = ("en", "de", "ru")
LOCALE_PATHS = [BASE_DIR / "locale"]
TIME_ZONE = os.environ.get("TIME_ZONE", "UTC")
USE_I18N = True
USE_TZ = True

# A missing translation may display the source text; public articles label its language.
MODELTRANSLATION_FALLBACK_LANGUAGES = ("ru", "en", "de")
