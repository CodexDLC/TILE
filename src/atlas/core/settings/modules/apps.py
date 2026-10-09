from importlib.util import find_spec

# ═══════════════════════════════════════════
# Application definition
# ═══════════════════════════════════════════

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
]

THIRD_PARTY_APPS = [
    "modeltranslation",
    # Auth
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "ninja",
]

if find_spec("unfold") is not None:
    THIRD_PARTY_APPS[5:5] = [
        "unfold",
        "unfold.contrib.filters",
        "unfold.contrib.forms",
        "unfold.contrib.inlines",
        "unfold.contrib.import_export",
        "unfold.contrib.guardian",
        "unfold.contrib.simple_history",
    ]

# ═══════════════════════════════════════════
# Codex Library Apps
# ═══════════════════════════════════════════
CODEX_APPS = [
    "codex_django.cabinet",
    "codex_django.messaging",
    "codex_django.showcase",
]

# ═══════════════════════════════════════════
# Codex Library Settings
# ═══════════════════════════════════════════
CODEX_SITE_SETTINGS_MODEL = "system.SiteSettings"
CODEX_STATIC_PAGE_SEO_MODEL = "system.StaticPageSeo"
MESSAGING_RECIPIENT_MODEL = "messaging.SystemRecipient"

LOCAL_APPS = [
    "cabinet",
    "core",
    "system",
    "features.content",
    "features.places",
    "features.contacts",
    "features.main",
    "features.messaging",
]

INSTALLED_APPS = CODEX_APPS + THIRD_PARTY_APPS + DJANGO_APPS + LOCAL_APPS
