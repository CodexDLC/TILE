from codex_django.cabinet import (
    CabinetResource,
    CabinetResourceField,
    CabinetResourceListColumn,
    SidebarItem,
    TopbarEntry,
    cabinet_resource_registry,
    declare,
)

from django.utils.translation import gettext_lazy as _

from .models import Page

CONTENT_MODULE = "content"


declare(
    module=CONTENT_MODULE,
    space="staff",
    topbar=TopbarEntry(
        group="admin",
        label=_("Content"),
        icon="bi-file-earmark-text",
        url="/cabinet/articles/",
        order=20,
    ),
    sidebar=[
        SidebarItem(
            label=_("Articles"),
            url="/cabinet/articles/",
            icon="bi-file-earmark-text",
            order=10,
            permissions=("content.view_page",),
        ),
        SidebarItem(
            label=_("Countries"),
            url="/cabinet/resources/places.country/",
            icon="bi-globe-europe-africa",
            order=20,
            permissions=("places.view_country",),
        ),
        SidebarItem(
            label=_("Regions"),
            url="/cabinet/resources/places.region/",
            icon="bi-map",
            order=30,
            permissions=("places.view_region",),
        ),
        SidebarItem(
            label=_("Cities"),
            url="/cabinet/resources/places.city/",
            icon="bi-buildings",
            order=40,
            permissions=("places.view_city",),
        ),
        SidebarItem(
            label="Места",
            url="/cabinet/resources/places.place/",
            icon="bi-geo-alt",
            order=50,
            permissions=("places.view_place",),
        ),
    ],
)


cabinet_resource_registry.register(
    CabinetResource(
        key="content.page",
        model=Page,
        section=CONTENT_MODULE,
        title="Страницы",
        singular_title="Страница",
        list_columns=[
            CabinetResourceListColumn("title", label="Название", searchable=True),
            CabinetResourceListColumn("page_type", label="Тип", searchable=True),
            CabinetResourceListColumn("slug", label="Slug", searchable=True),
            CabinetResourceListColumn("is_published", label="Опубликовано"),
            CabinetResourceListColumn("updated_at", label="Обновлено"),
        ],
        form_fields=[
            CabinetResourceField(
                "parent",
                label="Родительская страница",
                required=False,
                ai_enabled=False,
                tooltip="Определяет место страницы в иерархии сайта. Если оставить пустым, страница будет верхнего уровня.",
            ),
            CabinetResourceField(
                "page_type",
                label="Тип страницы",
                ai_enabled=False,
                tooltip="Выбирает публичный шаблон и поведение страницы: страна, регион, город, место или обычная страница.",
            ),
            CabinetResourceField(
                "title",
                label="Название",
                role="title",
                tooltip="Главный заголовок страницы. По нему автоматически создается URL.",
            ),
            CabinetResourceField(
                "intro",
                label="Вступление",
                role="lead",
                format="html",
                required=False,
                tooltip="Короткий вводный текст для первого экрана или начала страницы. Лучше держать его компактным.",
            ),
            CabinetResourceField(
                "template_hint",
                label="Шаблон",
                required=False,
                ai_enabled=False,
                tooltip="Необязательная подсказка для выбора варианта отображения, если одному типу страницы нужно несколько шаблонов.",
            ),
            CabinetResourceField(
                "is_published",
                label="Опубликовано",
                required=False,
                widget="toggle",
                ai_enabled=False,
                tooltip="Включает страницу на публичном сайте. Черновики остаются доступны только в кабинете.",
            ),
        ],
        create_enabled=True,
        create_label="Создать страницу",
        smart_create=False,
        smart_handler="features.content.services.smart_create.ContentSmartCreateHandler",
        base_language="ru",
        target_languages=("ru", "en", "de"),
    )
)

