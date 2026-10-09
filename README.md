# Atlas

Авторский атлас-путеводитель на Django. Здесь описан локальный запуск на Windows.

## Окружение

Используется Python 3.14 (ветка закреплена в `.python-version` и `pyproject.toml`).
Команды выполняйте через `uv`: системный Python может содержать другие версии библиотек.

Из корня проекта:

```powershell
Set-Location C:\install\projects\clients\atlas
uv sync --locked --extra dev
uv run --locked --extra dev manage check
uv run --locked --extra dev manage runserver
```

Откройте http://127.0.0.1:8000/ . Остановка сервера — Ctrl+C.
Команда `manage` также работает из `src\atlas`: повторно добавлять `src\atlas` к пути не нужно.
Если запускаете непосредственно файл из этой вложенной папки, используйте
`uv run --locked --extra dev python manage.py runserver`.

При первом запуске с новой базой выполните `uv run --locked --extra dev manage migrate`.
Это изменяет схему базы; для существующей базы сначала сделайте резервную копию.
Публичная главная страница требует опубликованной домашней страницы в базе.

## Свои библиотеки

Все шесть пакетов `codex-*` подключены в режиме editable из соседней папки:

```text
projects/
  clients/atlas/
  codex_tools/
    codex-ai/
    codex-core/
    codex-django/
    codex-django-cli/
    codex-platform/
    codex_services/
```

Локальные изменения библиотек сразу видны Atlas. Удалять эти папки после установки нельзя.
Их версии и зависимости учитывает `uv.lock`, но исходники editable-пакетов он не фиксирует.
После намеренного изменения зависимостей выполните `uv lock`, затем `uv sync --locked --extra dev`.
Для проверки именно опубликованных версий нужен отдельный проверенный набор зависимостей;
текущая конфигурация предназначена для локальной разработки с `codex_tools`.

## Настройки и IDE

Локальные настройки берутся из `.env`; перечень параметров приведён в `.env.example`.
Не публикуйте `.env` с паролями и ключами.

В PyCharm выберите интерпретатор `<корень проекта>\.venv\Scripts\python.exe`.
Для обычной Python-конфигурации запуска задайте:

- script: `<корень проекта>\src\atlas\manage.py`;
- parameters: `runserver`;
- working directory: корень проекта.

Сервер разработки использует настройки `atlas.core.settings.dev`.
Почта, фоновые очереди и ИИ требуют отдельной настройки; обычный запуск сервера не проверяет их доставку.

## Проверки

```powershell
uv run --locked --extra dev python -m pytest -q
uv run --locked --extra dev ruff check src tests
uv pip check --python .venv/Scripts/python.exe
```

Тесты используют SQLite в памяти, локальный кэш и почту в памяти.
В тестовых настройках отключены рабочие Redis/ARQ-подключения и файловые логи.
`django_debug_mode = true` сохраняет штатное отключение Redis в библиотеках при локальных тестах;
проверки поведения production должны явно переопределять настройки и подменять внешние сервисы.

`runserver` не пересобирает стили и скрипты. После их изменения используйте
`uv run --locked --extra dev manage compile_assets` или команду `manage startserver`,
которая выполняет сборку перед запуском. Сборка обновляет генерируемые файлы.
