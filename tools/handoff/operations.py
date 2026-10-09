"""Create and restore complete offline handoff archives."""

from __future__ import annotations

import json
import os
import tempfile
import zipfile
from pathlib import Path

from .archive import (
    DATABASE_NAME,
    FORMAT_VERSION,
    MANIFEST_NAME,
    HandoffError,
    copy_and_hash,
    extract_checked,
    media_files,
    require_plain_path,
    snapshot_database,
    verify_archive,
)


def _separate_paths(database: Path, media: Path, output: Path, staging: Path) -> None:
    database = database.resolve(strict=True)
    media = media.resolve(strict=True)
    output = output.resolve(strict=False)
    staging = staging.resolve(strict=True)
    if output == database or output == media or media in output.parents:
        raise HandoffError("Output must be outside the database and media source")
    if staging == media or media in staging.parents or staging == output.parent or output.parent in staging.parents:
        raise HandoffError("Staging must be separate from media and the output directory")
    if database == media or media in database.parents:
        raise HandoffError("Database must be outside the media directory")
    if output.parent.stat().st_dev != staging.stat().st_dev:
        raise HandoffError("Staging and output must be on the same filesystem for atomic publication")


def create_archive(database: Path, media: Path, output: Path, staging: Path, writers_stopped: bool) -> int:
    database, media, output, staging = (path.absolute() for path in (database, media, output, staging))
    if not writers_stopped:
        raise HandoffError("Confirm stopped database and media writers with --writers-stopped")
    if output.suffix.lower() != ".zip":
        raise HandoffError("Output must be a .zip file")
    if output.exists() or output.is_symlink():
        raise HandoffError(f"Output already exists: {output}")
    if not output.parent.is_dir() or not staging.is_dir():
        raise HandoffError("Output parent and staging directory must already exist")
    for path in (database, media, output.parent, staging):
        require_plain_path(path)
    _separate_paths(database, media, output, staging)
    files = media_files(media)
    with tempfile.TemporaryDirectory(prefix="atlas-handoff-", dir=staging) as scratch:
        scratch_path = Path(scratch)
        snapshot = scratch_path / DATABASE_NAME
        archive_path = scratch_path / "archive.zip"
        snapshot_database(database, snapshot)
        entries: dict[str, dict[str, object]] = {}
        with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED, allowZip64=True) as archive:
            for name, source_path in [(DATABASE_NAME, snapshot), *files]:
                require_plain_path(source_path)
                with source_path.open("rb") as source, archive.open(name, "w") as target:
                    size, digest = copy_and_hash(source, target)
                entries[name] = {"size": size, "sha256": digest}
            archive.writestr(MANIFEST_NAME, json.dumps({"format": FORMAT_VERSION, "files": entries}, sort_keys=True))
        verify_archive(archive_path)
        if output.exists() or output.is_symlink():
            raise HandoffError(f"Output appeared during backup: {output}")
        os.rename(archive_path, output)
    return len(files)


def restore_archive(archive_path: Path, target: Path) -> int:
    archive_path, target = archive_path.absolute(), target.absolute()
    if target.exists() or target.is_symlink():
        raise HandoffError(f"Restore target already exists: {target}")
    if not target.parent.is_dir():
        raise HandoffError(f"Restore target parent does not exist: {target.parent}")
    require_plain_path(target)
    require_plain_path(archive_path)
    if archive_path.absolute() == target.absolute() or target in archive_path.parents:
        raise HandoffError("Restore target must be separate from archive")
    with tempfile.TemporaryDirectory(prefix="atlas-handoff-restore-", dir=target.parent) as scratch:
        scratch_path = Path(scratch)
        restored = scratch_path / "restored"
        restored.mkdir()
        count = extract_checked(archive_path, restored)
        if target.exists() or target.is_symlink():
            raise HandoffError(f"Restore target appeared during validation: {target}")
        os.rename(restored, target)
    return count
