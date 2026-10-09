from __future__ import annotations

import json
import os
import sqlite3
import subprocess
import sys
import tempfile
import unittest
import warnings
import zipfile
from contextlib import closing
from pathlib import Path

from tools.handoff.archive import HandoffError, verify_archive
from tools.handoff.operations import create_archive, restore_archive


class HandoffTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.database = self.root / "working.sqlite3"
        self.media = self.root / "media"
        (self.media / "articles").mkdir(parents=True)
        (self.media / "articles" / "photo.jpg").write_bytes(b"test photo bytes")
        with closing(sqlite3.connect(self.database)) as connection:
            with connection:
                connection.execute("CREATE TABLE story (title TEXT NOT NULL)")
                connection.execute("INSERT INTO story VALUES (?)", ("Sample",))
        self.output_dir = self.root / "finished"
        self.staging = self.root / "private-staging"
        self.output_dir.mkdir()
        self.staging.mkdir()
        self.archive = self.output_dir / "handoff.zip"

    def create(self) -> None:
        create_archive(self.database, self.media, self.archive, self.staging, True)

    def test_round_trip_and_source_untouched(self) -> None:
        original_db = self.database.read_bytes()
        original_photo = (self.media / "articles" / "photo.jpg").read_bytes()
        self.create()
        self.assertEqual(verify_archive(self.archive), 1)
        target = self.root / "new-owner"
        self.assertEqual(restore_archive(self.archive, target), 1)
        with closing(sqlite3.connect(target / "database.sqlite3")) as connection:
            self.assertEqual(connection.execute("SELECT title FROM story").fetchone(), ("Sample",))
        self.assertEqual((target / "media" / "articles" / "photo.jpg").read_bytes(), original_photo)
        self.assertEqual(self.database.read_bytes(), original_db)
        self.assertEqual((self.media / "articles" / "photo.jpg").read_bytes(), original_photo)
        self.assertEqual(list(self.staging.iterdir()), [])

    def test_requires_stopped_writers_and_refuses_overwrite(self) -> None:
        with self.assertRaises(HandoffError):
            create_archive(self.database, self.media, self.archive, self.staging, False)
        self.create()
        with self.assertRaises(HandoffError):
            self.create()
        target = self.root / "existing"
        target.mkdir()
        (target / "keep.txt").write_text("untouched")
        with self.assertRaises(HandoffError):
            restore_archive(self.archive, target)
        self.assertEqual((target / "keep.txt").read_text(), "untouched")

    def test_output_path_with_parent_segment_cannot_enter_media(self) -> None:
        disguised_output = self.output_dir / ".." / "media" / "archive.zip"
        with self.assertRaises(HandoffError):
            create_archive(self.database, self.media, disguised_output, self.staging, True)
        self.assertFalse((self.media / "archive.zip").exists())

    def test_corruption_is_rejected_without_publishing_restore(self) -> None:
        self.create()
        damaged = self.root / "damaged.zip"
        with zipfile.ZipFile(self.archive) as source, zipfile.ZipFile(damaged, "w") as output:
            for item in source.infolist():
                data = source.read(item.filename)
                if item.filename == "media/articles/photo.jpg":
                    data = b"changed"
                output.writestr(item, data)
        with self.assertRaisesRegex(HandoffError, "Checksum mismatch"):
            verify_archive(damaged)
        target = self.root / "failed-restore"
        with self.assertRaisesRegex(HandoffError, "Checksum mismatch"):
            restore_archive(damaged, target)
        self.assertFalse(target.exists())

    def test_traversal_and_duplicate_members_are_rejected(self) -> None:
        for member in ("../escape", "/absolute", "media/../escape", "media\\escape"):
            with self.subTest(member=member):
                unsafe = self.root / "unsafe.zip"
                with zipfile.ZipFile(unsafe, "w") as archive:
                    archive.writestr(member, b"x")
                    archive.writestr(
                        "manifest.json",
                        json.dumps(
                            {
                                "format": 1,
                                "files": {"database.sqlite3": {"size": 0, "sha256": "0" * 64}},
                            }
                        ),
                    )
                with self.assertRaises(HandoffError):
                    verify_archive(unsafe)
        duplicate = self.root / "duplicate.zip"
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            with zipfile.ZipFile(duplicate, "w") as archive:
                archive.writestr("database.sqlite3", b"one")
                archive.writestr("database.sqlite3", b"two")
                archive.writestr("manifest.json", "{}")
        with self.assertRaisesRegex(HandoffError, "duplicate"):
            verify_archive(duplicate)

    def test_source_links_and_environment_files_are_rejected(self) -> None:
        (self.media / ".env").write_text("SECRET=do-not-copy")
        with self.assertRaisesRegex(HandoffError, "environment file"):
            self.create()
        self.assertFalse(self.archive.exists())
        (self.media / ".env").unlink()
        try:
            (self.media / "link.jpg").symlink_to(self.media / "articles" / "photo.jpg")
        except OSError, NotImplementedError:
            self.skipTest("Creating symlinks is unavailable")
        with self.assertRaisesRegex(HandoffError, "Link or reparse point"):
            self.create()
        self.assertFalse(self.archive.exists())

    def test_relative_cli_paths_with_spaces_and_empty_media(self) -> None:
        base = self.root / "relative paths"
        base.mkdir()
        (base / "empty media").mkdir()
        (base / "finished archives").mkdir()
        (base / "private staging").mkdir()
        database = base / "database with spaces.sqlite3"
        with closing(sqlite3.connect(database)) as connection:
            connection.execute("CREATE TABLE check_me (value TEXT)")
        env = dict(os.environ, PYTHONPATH=str(Path(__file__).resolve().parents[3]))

        def run_cli(*arguments: str) -> subprocess.CompletedProcess[str]:
            # Fixed interpreter and module; arguments are synthetic local fixtures.
            return subprocess.run(  # noqa: S603
                [sys.executable, "-B", "-m", "tools.handoff", *arguments],
                cwd=base,
                env=env,
                capture_output=True,
                text=True,
            )

        created = run_cli(
            "create",
            "--database",
            database.name,
            "--media",
            "empty media",
            "--staging",
            "private staging",
            "--output",
            "finished archives/backup.zip",
            "--writers-stopped",
        )
        self.assertEqual(created.returncode, 0, created.stderr)
        verified = run_cli("verify", "finished archives/backup.zip")
        self.assertEqual(verified.returncode, 0, verified.stderr)
        restored = run_cli("restore", "finished archives/backup.zip", "--target", "new restore")
        self.assertEqual(restored.returncode, 0, restored.stderr)
        self.assertTrue((base / "new restore" / "media").is_dir())
        self.assertTrue((base / "new restore" / "database.sqlite3").is_file())


if __name__ == "__main__":
    unittest.main()
