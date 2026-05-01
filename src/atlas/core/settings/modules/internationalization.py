import os
from pathlib import Path

# Root of Django project: src/backend_django
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

# ═══════════════════════════════════════════
# Internationalization
# ═══════════════════════════════════════════

LANGUAGE_CODE = os.environ.get("LANGUAGE_CODE", "en")
TIME_ZONE = os.environ.get("TIME_ZONE", "UTC")
USE_I18N = False
USE_TZ = True
