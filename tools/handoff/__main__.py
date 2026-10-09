"""Command line entry point: python -m tools.handoff."""

from __future__ import annotations

import argparse
from pathlib import Path

from .archive import HandoffError, verify_archive
from .operations import create_archive, restore_archive


def main() -> int:
    parser = argparse.ArgumentParser(description="Offline Atlas SQLite and media handoff")
    commands = parser.add_subparsers(dest="command", required=True)
    create = commands.add_parser("create", help="Create a verified backup archive")
    create.add_argument("--database", type=Path, required=True)
    create.add_argument("--media", type=Path, required=True)
    create.add_argument("--output", type=Path, required=True)
    create.add_argument("--staging", type=Path, required=True, help="Existing directory outside the synced output")
    create.add_argument("--writers-stopped", action="store_true", help="Confirm database and photo writes have stopped")
    verify = commands.add_parser("verify", help="Check checksums and SQLite integrity")
    verify.add_argument("archive", type=Path)
    restore = commands.add_parser("restore", help="Restore to a new path only")
    restore.add_argument("archive", type=Path)
    restore.add_argument("--target", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == "create":
            count = create_archive(args.database, args.media, args.output, args.staging, args.writers_stopped)
            print(f"Created and verified {args.output} with {count} media files")
        elif args.command == "verify":
            count = verify_archive(args.archive)
            print(f"Verified {args.archive} with {count} media files")
        else:
            count = restore_archive(args.archive, args.target)
            print(f"Restored {count} media files to {args.target}")
    except (HandoffError, OSError) as exc:
        parser.exit(2, f"Handoff error: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
