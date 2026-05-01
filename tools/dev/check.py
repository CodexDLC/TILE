import sys
from pathlib import Path

try:
    from codex_core.dev.check_runner import BaseCheckRunner
except ImportError:
    print("Error: codex-core is required for the checker. Run 'uv sync --extra dev' before using tools/dev/check.py.")
    sys.exit(1)


class CheckRunner(BaseCheckRunner):
    """Thin launcher; project policy lives in pyproject.toml."""


if __name__ == "__main__":
    CheckRunner(Path(__file__).parent.parent.parent).main()
