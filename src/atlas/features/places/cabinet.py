# ruff: noqa: RUF001

from codex_django.cabinet import (
    CabinetResource,
    CabinetResourceField,
    CabinetResourceListColumn,
    cabinet_resource_registry,
)

from .models import City, Country, Place, Region

CONTENT_MODULE = "content"
SMART_HANDLER = "features.content.services.smart_create.ContentSmartCreateHandler"
BASE_LANGUAGE = "ru"


cabinet_resource_registry.register(
    CabinetResource(
        key="places.country",
        model=Country,
        section=CONTENT_MODULE,
        title="Страны",
        singular_title="Страна",
        list_columns=[
            CabinetResourceListColumn("name", label="Название", searchable=True),
            CabinetResourceListColumn("slug", label="Slug", searchable=True),
            CabinetResourceListColumn("page", label="Страница"),
            CabinetResourceListColumn("updated_at", label="Обновлено"),
        ],
        form_fields=[
            CabinetResourceField(
                "page",
                label="Связанная страница",
                required=False,
                ai_enabled=False,
                tooltip="Техническая связь с CMS-страницей. Можно оставить пустой, если страница будет создана позже.",
            ),
            CabinetResourceField(
                "name",
                label="Название",
                role="title",
                tooltip="Название страны. По нему автоматически создается slug и переводы.",
            ),
            CabinetResourceField(
                "intro",
                label="Вступление",
                role="lead",
                format="html",
                required=False,
                tooltip="Короткое описание страны для верхней части страницы. Не SEO description.",
            ),
        ],
        create_label="Создать страну",
        smart_create=True,
        smart_handler=SMART_HANDLER,
        base_language=BASE_LANGUAGE,
    )
)


cabinet_resource_registry.register(
    CabinetResource(
        key="places.region",
        model=Region,
        section=CONTENT_MODULE,
        title="Регионы",
        singular_title="Регион",
        list_columns=[
            CabinetResourceListColumn("name", label="Название", searchable=True),
            CabinetResourceListColumn("country", label="Страна"),
            CabinetResourceListColumn("slug", label="Slug", searchable=True),
            CabinetResourceListColumn("page", label="Страница"),
            CabinetResourceListColumn("updated_at", label="Обновлено"),
        ],
        form_fields=[
            CabinetResourceField(
                "country",
                label="Страна",
                ai_enabled=False,
                tooltip="Страна, к которой относится регион. Это поле не переводится.",
            ),
            CabinetResourceField(
                "page",
                label="Связанная страница",
                required=False,
                ai_enabled=False,
                tooltip="Техническая связь с CMS-страницей. Можно оставить пустой, если страница будет создана позже.",
            ),
            CabinetResourceField(
                "name",
                label="Название",
                role="title",
                tooltip="Название региона. По нему автоматически создается slug и переводы.",
            ),
            CabinetResourceField(
                "intro",
                label="Вступление",
                role="lead",
                format="html",
                required=False,
                tooltip="Короткое описание региона для верхней части страницы. Не SEO description.",
            ),
        ],
        create_label="Создать регион",
        smart_create=True,
        smart_handler=SMART_HANDLER,
        base_language=BASE_LANGUAGE,
    )
)


cabinet_resource_registry.register(
    CabinetResource(
        key="places.city",
        model=City,
        section=CONTENT_MODULE,
        title="Города",
        singular_title="Город",
        list_columns=[
            CabinetResourceListColumn("name", label="Название", searchable=True),
            CabinetResourceListColumn("region", label="Регион"),
            CabinetResourceListColumn("slug", label="Slug", searchable=True),
            CabinetResourceListColumn("page", label="Страница"),
            CabinetResourceListColumn("updated_at", label="Обновлено"),
        ],
        form_fields=[
            CabinetResourceField(
                "region",
                label="Регион",
                ai_enabled=False,
                tooltip="Регион, к которому относится город. Это поле не переводится.",
            ),
            CabinetResourceField(
                "page",
                label="Связанная страница",
                required=False,
                ai_enabled=False,
                tooltip="Техническая связь с CMS-страницей. Можно оставить пустой, если страница будет создана позже.",
            ),
            CabinetResourceField(
                "name",
                label="Название",
                role="title",
                tooltip="Название города. По нему автоматически создается slug и переводы.",
            ),
            CabinetResourceField(
                "intro",
                label="Вступление",
                role="lead",
                format="html",
                required=False,
                tooltip="Короткое описание города для верхней части страницы. Не SEO description.",
            ),
        ],
        create_label="Создать город",
        smart_create=True,
        smart_handler=SMART_HANDLER,
        base_language=BASE_LANGUAGE,
    )
)


cabinet_resource_registry.register(
    CabinetResource(
        key="places.place",
        model=Place,
        section=CONTENT_MODULE,
        title="Места",
        singular_title="Место",
        list_columns=[
            CabinetResourceListColumn("name", label="Название", searchable=True),
            CabinetResourceListColumn("city", label="Город"),
            CabinetResourceListColumn("slug", label="Slug", searchable=True),
            CabinetResourceListColumn("seasonality", label="Сезонность", searchable=True),
            CabinetResourceListColumn("updated_at", label="Обновлено"),
        ],
        form_fields=[
            CabinetResourceField(
                "city",
                label="Город",
                ai_enabled=False,
                tooltip="Город, к которому относится место. Это поле не переводится.",
            ),
            CabinetResourceField(
                "page",
                label="Связанная страница",
                required=False,
                ai_enabled=False,
                tooltip="Техническая связь с CMS-страницей. Можно оставить пустой, если страница будет создана позже.",
            ),
            CabinetResourceField(
                "name",
                label="Название",
                role="title",
                tooltip="Название места. По нему автоматически создается slug и переводы.",
            ),
            CabinetResourceField(
                "intro",
                label="Вступление",
                role="lead",
                format="html",
                required=False,
                tooltip="Короткое описание места для верхней части страницы. Не SEO description.",
            ),
            CabinetResourceField(
                "long_form_story",
                label="Большой текст / история",
                role="body",
                format="html",
                required=False,
                tooltip="Основной длинный текст о месте. Его можно улучшать, форматировать и переводить через Preview.",
            ),
            CabinetResourceField(
                "seasonality",
                label="Сезонность",
                required=False,
                tooltip="Короткая фраза про лучший сезон: например, Весна-осень или Круглый год.",
            ),
            CabinetResourceField(
                "seasonality_text",
                label="Текст о сезонности",
                role="body",
                format="html",
                required=False,
                tooltip="Короткое объяснение, когда лучше посещать место и почему.",
            ),
            CabinetResourceField("latitude", label="Широта", required=False, ai_enabled=False),
            CabinetResourceField("longitude", label="Долгота", required=False, ai_enabled=False),
        ],
        create_label="Создать место",
        smart_create=True,
        smart_handler=SMART_HANDLER,
        base_language=BASE_LANGUAGE,
    )
)
