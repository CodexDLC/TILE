# TALE / atlas

Публичный бренд — TALE; внутреннее имя проекта — atlas.

## Цель и границы

MVP 1: автор вручную создаёт, просматривает и публикует статьи с фотографиями; читатель находит город и читает истории. Аудио/монетизация — MVP 2 после трафика. Планы не являются разрешением внедрять будущие функции.

Сохранять пользовательские изменения, рабочие данные и опубликованные URL. Не читать секреты и не выполнять наполнение/миграцию рабочих данных ради демонстрации. Глобальные правила делегирования и полномочий не дублировать здесь; прямое указание владельца о последовательной работе имеет приоритет.

## Рабочий режим

Для выбора языка объяснений и границы авторских изменений схемы читать `.agents/skills/atlas-working-modes/SKILL.md`. Известный в текущем разговоре режим сохраняется; в новой сессии следовать правилу определения режима из навыка.

## Навыки по задаче

Пути ниже относительно корня репозитория. Читать только нужные навыки, не весь каталог.

| Задача | Навык |
| --- | --- |
| Локальный запуск для автора, обновления и резервные копии | .agents/skills/atlas-local-operations/SKILL.md |
| Определить область изменения/проверки | .agents/skills/atlas-change-triage/SKILL.md |
| Модули, чтение/запись, модели, интеграции | .agents/skills/atlas-architecture/SKILL.md |
| Статьи, языки, публикация, Page и блоки | .agents/skills/atlas-page-blocks/SKILL.md |
| Кабинет автора и подключение общей оболочки | .agents/skills/atlas-cabinet-feature-change/SKILL.md |
| Публичные страницы, поиск и навигация | .agents/skills/atlas-public-template-change/SKILL.md |
| Визуальные изменения, CSS/JS и сборка | .agents/skills/atlas-design-system/SKILL.md |

При изменении codex_django API найти usage-skill установленной библиотеки и прочитать только соответствующий reference. Проектные инструкции описывают правила TALE, а не копируют библиотечные API. Если окружение или путь библиотеки сломан, сначала сообщить наблюдаемую причину, не подменять источник пакетом другой версии.

## Приёмка

Проверять затронутые сценарии и реальные права редактора. Для значимых UI-изменений нужны актуальные desktop/mobile снимки и проверка взаимодействий; зелёные Django-тесты не доказывают удобство. Разделять выполненные изменения, проверенные факты, предложения и непроверенные ограничения.


## Переносимость навыков

Проектные навыки в .agents/skills/ и проектный AGENTS.md переносятся вместе с репозиторием через Git. Архивы и резервные копии навыков — статичные снимки для ручного переноса и не являются активными инструкциями.

<!-- codex-ai:skill:start -->
<!-- codex-ai:skill:separator=0 -->
Use [codex-ai](.agents/skills/codex-ai/SKILL.md) for codex_ai work.
<!-- codex-ai:skill:end -->
<!-- codex-core:skill:start -->
<!-- codex-core:skill:separator=0 -->
Use [codex-core](.agents/skills/codex-core/SKILL.md) for codex_core work.
<!-- codex-core:skill:end -->
<!-- codex-django:skill:start -->
<!-- codex-django:skill:separator=0 -->
Use [codex-django](.agents/skills/codex-django/SKILL.md) for codex_django work.
<!-- codex-django:skill:end -->
<!-- codex-django-cli:skill:start -->
<!-- codex-django-cli:skill:separator=0 -->
Use [codex-django-cli](.agents/skills/codex-django-cli/SKILL.md) for codex_django_cli work.
<!-- codex-django-cli:skill:end -->
<!-- codex-platform:skill:start -->
<!-- codex-platform:skill:separator=0 -->
Use [codex-platform](.agents/skills/codex-platform/SKILL.md) for codex_platform work.
<!-- codex-platform:skill:end -->
<!-- codex-services:skill:start -->
<!-- codex-services:skill:separator=0 -->
Use [codex-services](.agents/skills/codex-services/SKILL.md) for codex_services work.
<!-- codex-services:skill:end -->
