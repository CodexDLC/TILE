from io import StringIO
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

import pytest
from django.core.management.base import CommandError

from atlas.system.management.commands import compile_assets


@pytest.fixture
def compilation(monkeypatch):
    config_path = Path("static/compiler_config.json")
    compiler = Mock()
    monkeypatch.setattr("codex_core.dev.static_compiler.StaticCompiler", lambda: compiler)
    monkeypatch.setattr(compile_assets, "settings", SimpleNamespace(STATICFILES_DIRS=["static"]))
    monkeypatch.setattr(compile_assets.apps, "get_app_configs", lambda: [])
    monkeypatch.setattr(Path, "rglob", lambda self, pattern: iter([config_path]))
    output = StringIO()
    return compile_assets.Command(stdout=output), compiler, config_path, output


def test_failed_compilation_raises_command_error(compilation):
    command, compiler, config_path, output = compilation
    compiler.compile_from_config.return_value = False

    with pytest.raises(CommandError, match="Static asset compilation failed") as error:
        command.handle()

    assert str(config_path) in str(error.value)
    assert "Static Assets Ready" not in output.getvalue()
    compiler.compile_from_config.assert_called_once_with(config_path)


def test_successful_compilation_reports_ready(compilation):
    command, compiler, config_path, output = compilation
    compiler.compile_from_config.return_value = True

    command.handle()

    compiler.compile_from_config.assert_called_once_with(config_path)
    assert "Static Assets Ready" in output.getvalue()
