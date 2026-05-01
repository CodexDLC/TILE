import os
from pathlib import Path

from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

# Root of Django project: src/backend_django
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
PROJECT_NAME = os.environ.get("PROJECT_NAME", BASE_DIR.name)


def _admin_link(app_label: str, model_name: str) -> str:
    return reverse_lazy(f"admin:{app_label}_{model_name}_changelist")


def _can_access_model(app_label: str, model_name: str):
    def checker(request):
        return any(
            request.user.has_perm(f"{app_label}.{action}_{model_name}")
            for action in ("view", "change", "add")
        )

    return checker

UNFOLD = {
    "SITE_TITLE": os.environ.get("ADMIN_SITE_TITLE", f"{PROJECT_NAME.replace('_', ' ').title()} Админка"),
    "SITE_HEADER": os.environ.get("ADMIN_SITE_HEADER", f"{PROJECT_NAME.replace('_', ' ').title()} админка"),
    "SITE_SYMBOL": "dashboard",
    "COLORS": {
        "primary": {
            "50": "239, 246, 255",
            "100": "219, 234, 254",
            "200": "191, 219, 254",
            "300": "147, 197, 253",
            "400": "96, 165, 250",
            "500": "59, 130, 246",
            "600": "37, 99, 235",
            "700": "29, 78, 216",
            "800": "30, 64, 175",
            "900": "30, 58, 138",
            "950": "23, 37, 84",
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        "navigation": [
            {
                "title": _("Основное"),
                "items": [
                    {
                        "title": _("Страницы"),
                        "icon": "article",
                        "link": _admin_link("content", "page"),
                        "permission": _can_access_model("content", "page"),
                    },
                    {
                        "title": _("Места"),
                        "icon": "place",
                        "link": _admin_link("places", "place"),
                        "permission": _can_access_model("places", "place"),
                    },
                    {
                        "title": _("Обращения"),
                        "icon": "forum",
                        "link": _admin_link("messaging", "thread"),
                        "permission": _can_access_model("messaging", "thread"),
                    },
                    {
                        "title": _("Получатели"),
                        "icon": "alternate_email",
                        "link": _admin_link("messaging", "systemrecipient"),
                        "permission": _can_access_model("messaging", "systemrecipient"),
                    },
                    {
                        "title": _("Кампании"),
                        "icon": "campaign",
                        "link": _admin_link("messaging", "campaign"),
                        "permission": _can_access_model("messaging", "campaign"),
                    },
                    {
                        "title": _("Настройки email"),
                        "icon": "mail_lock",
                        "link": _admin_link("system", "emailsettings"),
                        "permission": _can_access_model("system", "emailsettings"),
                    },
                    {
                        "title": _("Настройки сайта"),
                        "icon": "settings",
                        "link": _admin_link("system", "sitesettings"),
                        "permission": _can_access_model("system", "sitesettings"),
                    },
                    {
                        "title": _("SEO страниц"),
                        "icon": "search",
                        "link": _admin_link("system", "staticpageseo"),
                        "permission": _can_access_model("system", "staticpageseo"),
                    },
                ],
            },
            {
                "title": _("Люди и доступ"),
                "items": [
                    {
                        "title": _("Пользователи"),
                        "icon": "person",
                        "link": _admin_link("auth", "user"),
                        "permission": _can_access_model("auth", "user"),
                    },
                    {
                        "title": _("Профили пользователей"),
                        "icon": "badge",
                        "link": _admin_link("system", "userprofile"),
                        "permission": _can_access_model("system", "userprofile"),
                    },
                    {
                        "title": _("Группы"),
                        "icon": "groups",
                        "link": _admin_link("auth", "group"),
                        "permission": _can_access_model("auth", "group"),
                    },
                ],
            },
            {
                "title": _("Контент"),
                "items": [
                    {
                        "title": _("Страницы"),
                        "icon": "article",
                        "link": _admin_link("content", "page"),
                        "permission": _can_access_model("content", "page"),
                    },
                    {
                        "title": _("Страны"),
                        "icon": "public",
                        "link": _admin_link("places", "country"),
                        "permission": _can_access_model("places", "country"),
                    },
                    {
                        "title": _("Регионы"),
                        "icon": "travel_explore",
                        "link": _admin_link("places", "region"),
                        "permission": _can_access_model("places", "region"),
                    },
                    {
                        "title": _("Города"),
                        "icon": "location_city",
                        "link": _admin_link("places", "city"),
                        "permission": _can_access_model("places", "city"),
                    },
                    {
                        "title": _("Места"),
                        "icon": "place",
                        "link": _admin_link("places", "place"),
                        "permission": _can_access_model("places", "place"),
                    },
                    {
                        "title": _("SEO страниц"),
                        "icon": "search",
                        "link": _admin_link("system", "staticpageseo"),
                        "permission": _can_access_model("system", "staticpageseo"),
                    },
                    {
                        "title": _("Статичные переводы"),
                        "icon": "translate",
                        "link": _admin_link("system", "statictranslation"),
                        "permission": _can_access_model("system", "statictranslation"),
                    },
                ],
            },
            {
                "title": _("Система и настройки"),
                "items": [
                    {
                        "title": _("Статичные переводы"),
                        "icon": "translate",
                        "link": _admin_link("system", "statictranslation"),
                        "permission": _can_access_model("system", "statictranslation"),
                    },
                    {
                        "title": _("Логи email"),
                        "icon": "receipt_long",
                        "link": _admin_link("messaging", "emaillog"),
                        "permission": _can_access_model("messaging", "emaillog"),
                    },
                ],
            },
        ],
    },
}
