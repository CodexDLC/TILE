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
    "SITE_TITLE": os.environ.get("ADMIN_SITE_TITLE", f"{PROJECT_NAME.replace('_', ' ').title()} Admin"),
    "SITE_HEADER": os.environ.get("ADMIN_SITE_HEADER", PROJECT_NAME.replace("_", " ").title()),
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
        "show_all_applications": False,
        "navigation": [
            {
                "title": _("Workspace"),
                "items": [
                    {
                        "title": _("Dashboard"),
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                    },
                ],
            },
            {
                "title": _("Workflows"),
                "items": [
                    {
                        "title": _("Message threads"),
                        "icon": "forum",
                        "link": _admin_link("messaging", "thread"),
                        "permission": _can_access_model("messaging", "thread"),
                    },
                    {
                        "title": _("Recipients"),
                        "icon": "alternate_email",
                        "link": _admin_link("messaging", "systemrecipient"),
                        "permission": _can_access_model("messaging", "systemrecipient"),
                    },
                    {
                        "title": _("Campaigns"),
                        "icon": "campaign",
                        "link": _admin_link("messaging", "campaign"),
                        "permission": _can_access_model("messaging", "campaign"),
                    },
                    {
                        "title": _("Email settings"),
                        "icon": "mail_lock",
                        "link": _admin_link("system", "emailsettings"),
                        "permission": _can_access_model("system", "emailsettings"),
                    },
                    {
                        "title": _("Site settings"),
                        "icon": "settings",
                        "link": _admin_link("system", "sitesettings"),
                        "permission": _can_access_model("system", "sitesettings"),
                    },
                    {
                        "title": _("SEO pages"),
                        "icon": "search",
                        "link": _admin_link("system", "staticpageseo"),
                        "permission": _can_access_model("system", "staticpageseo"),
                    },
                ],
            },
            {
                "title": _("People & Access"),
                "items": [
                    {
                        "title": _("Users"),
                        "icon": "person",
                        "link": _admin_link("auth", "user"),
                        "permission": _can_access_model("auth", "user"),
                    },
                    {
                        "title": _("User profiles"),
                        "icon": "badge",
                        "link": _admin_link("system", "userprofile"),
                        "permission": _can_access_model("system", "userprofile"),
                    },
                    {
                        "title": _("Groups"),
                        "icon": "groups",
                        "link": _admin_link("auth", "group"),
                        "permission": _can_access_model("auth", "group"),
                    },
                ],
            },
            {
                "title": _("All models"),
                "items": [
                    {
                        "title": _("System domain"),
                        "icon": "settings",
                        "items": [
                            {
                                "title": _("Site settings"),
                                "link": _admin_link("system", "sitesettings"),
                                "permission": _can_access_model("system", "sitesettings"),
                            },
                            {
                                "title": _("Email settings"),
                                "link": _admin_link("system", "emailsettings"),
                                "permission": _can_access_model("system", "emailsettings"),
                            },
                            {
                                "title": _("SEO pages"),
                                "link": _admin_link("system", "staticpageseo"),
                                "permission": _can_access_model("system", "staticpageseo"),
                            },
                            {
                                "title": _("Static translations"),
                                "link": _admin_link("system", "statictranslation"),
                                "permission": _can_access_model("system", "statictranslation"),
                            },
                            {
                                "title": _("User profiles"),
                                "link": _admin_link("system", "userprofile"),
                                "permission": _can_access_model("system", "userprofile"),
                            },
                        ],
                    },
                    {
                        "title": _("Messaging domain"),
                        "icon": "mail",
                        "items": [
                            {
                                "title": _("Threads"),
                                "link": _admin_link("messaging", "thread"),
                                "permission": _can_access_model("messaging", "thread"),
                            },
                            {
                                "title": _("Messages"),
                                "link": _admin_link("messaging", "message"),
                                "permission": _can_access_model("messaging", "message"),
                            },
                            {
                                "title": _("Replies"),
                                "link": _admin_link("messaging", "messagereply"),
                                "permission": _can_access_model("messaging", "messagereply"),
                            },
                            {
                                "title": _("Recipients"),
                                "link": _admin_link("messaging", "systemrecipient"),
                                "permission": _can_access_model("messaging", "systemrecipient"),
                            },
                            {
                                "title": _("Email logs"),
                                "link": _admin_link("messaging", "emaillog"),
                                "permission": _can_access_model("messaging", "emaillog"),
                            },
                            {
                                "title": _("Campaigns"),
                                "link": _admin_link("messaging", "campaign"),
                                "permission": _can_access_model("messaging", "campaign"),
                            },
                            {
                                "title": _("Campaign recipients"),
                                "link": _admin_link("messaging", "campaignrecipient"),
                                "permission": _can_access_model("messaging", "campaignrecipient"),
                            },
                        ],
                    },
                    {
                        "title": _("Accounts"),
                        "icon": "manage_accounts",
                        "items": [
                            {
                                "title": _("Users"),
                                "link": _admin_link("auth", "user"),
                                "permission": _can_access_model("auth", "user"),
                            },
                            {
                                "title": _("Groups"),
                                "link": _admin_link("auth", "group"),
                                "permission": _can_access_model("auth", "group"),
                            },
                        ],
                    },
                    {
                        "title": _("Editorial"),
                        "icon": "edit_note",
                        "items": [
                            {
                                "title": _("Static translations"),
                                "link": _admin_link("system", "statictranslation"),
                                "permission": _can_access_model("system", "statictranslation"),
                            },
                            {
                                "title": _("SEO pages"),
                                "link": _admin_link("system", "staticpageseo"),
                                "permission": _can_access_model("system", "staticpageseo"),
                            },
                        ],
                    },
                ],
            },
            {
                "title": _("System & Settings"),
                "items": [
                    {
                        "title": _("Static translations"),
                        "icon": "translate",
                        "link": _admin_link("system", "statictranslation"),
                        "permission": _can_access_model("system", "statictranslation"),
                    },
                    {
                        "title": _("Email logs"),
                        "icon": "receipt_long",
                        "link": _admin_link("messaging", "emaillog"),
                        "permission": _can_access_model("messaging", "emaillog"),
                    },
                ],
            },
        ],
    },
}
