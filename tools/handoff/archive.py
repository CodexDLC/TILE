"""Archive format, source checks, and streaming verification."""

from __future__ import annotations

import hashlib
import json
import os
import sqlite3
import stat
import tempfile
import zipfile
from contextlib import closing
from pathlib import Path, PurePosixPath

DATABASE_NAME = "database.sqlite3"
MANIFEST_NAME = "manifest.json"
FORMAT_VERSION = 1
CHUNK_SIZE = 1024 * 1024


class HandoffError(Exception):
    """An unsafe or invalid handoff operation."""


def _is_link(path: Path) -> bool:
    if path.is_symlink():
        return True
    return os.name == "nt" and bool(path.lstat().st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT)


def require_plain_path(path: Path) -> None:
    """Reject links and Windows reparse points anywhere in an existing path."""
    if ".." in path.parts:
        raise HandoffError(f"Parent path segments are not allowed: {path}")
    current = path.absolute()
    for part in (current, *current.parents):
        if part.exists() or part.is_symlink():
            if _is_link(part):
                raise HandoffError(f"Link or reparse point is not allowed: {part}")


def media_files(media: Path) -> list[tuple[str, Path]]:
    if not media.is_dir():
        raise HandoffError(f"Media directory does not exist: {media}")
    require_plain_path(media)
    found: list[tuple[str, Path]] = []
    for root, dirs, files in os.walk(media, followlinks=False):
        base = Path(root)
        for name in dirs + files:
            item = base / name
            require_plain_path(item)
            if name == ".env" or name.startswith(".env."):
                raise HandoffError(f"Refusing environment file in media: {item}")
        for name in files:
            item = base / name
            if not item.is_file():
                raise HandoffError(f"Media entry is not a regular file: {item}")
            relative = item.relative_to(media).as_posix()
            archive_name = f"media/{relative}"
            checked_member(archive_name)
            found.append((archive_name, item))
    found.sort(key=lambda pair: pair[0])
    return found


def checked_member(name: str) -> None:
    if not isinstance(name, str) or not name or "\\" in name or "\x00" in name or ":" in name:
        raise HandoffError(f"Unsafe archive member: {name!r}")
    path = PurePosixPath(name)
    if name.startswith("/") or any(part in ("", ".", "..") for part in name.split("/")) or str(path) != name:
        raise HandoffError(f"Unsafe archive member: {name!r}")


def copy_and_hash(source, destination) -> tuple[int, str]:
    digest = hashlib.sha256()
    size = 0
    while chunk := source.read(CHUNK_SIZE):
        destination.write(chunk)
        digest.update(chunk)
        size += len(chunk)
    return size, digest.hexdigest()


def sqlite_integrity(database: Path) -> None:
    try:
        with closing(sqlite3.connect(database.as_uri() + "?mode=ro", uri=True)) as connection:
            result = connection.execute("PRAGMA integrity_check").fetchone()
        if result != ("ok",):
            raise HandoffError(f"SQLite integrity check failed: {result!r}")
    except sqlite3.DatabaseError as exc:
        raise HandoffError(f"Invalid SQLite database: {exc}") from exc


def snapshot_database(source: Path, destination: Path) -> None:
    if not source.is_file():
        raise HandoffError(f"Database file does not exist: {source}")
    require_plain_path(source)
    try:
        with closing(sqlite3.connect(source.as_uri() + "?mode=ro", uri=True)) as original:
            with closing(sqlite3.connect(destination)) as snapshot:
                original.backup(snapshot)
        sqlite_integrity(destination)
    except sqlite3.DatabaseError as exc:
        raise HandoffError(f"Could not snapshot SQLite database: {exc}") from exc


def _entry(info: zipfile.ZipInfo) -> None:
    checked_member(info.filename)
    if info.is_dir() or stat.S_ISLNK(info.external_attr >> 16):
        raise HandoffError(f"Archive contains a directory or link: {info.filename}")


def archive_entries(archive: zipfile.ZipFile) -> dict[str, dict[str, object]]:
    infos = archive.infolist()
    names = [info.filename for info in infos]
    if len(names) != len(set(names)):
        raise HandoffError("Archive contains duplicate members")
    for info in infos:
        _entry(info)
    if MANIFEST_NAME not in names:
        raise HandoffError("Archive has no manifest")
    try:
        with archive.open(MANIFEST_NAME) as source:
            raw = source.read(1024 * 1024 + 1)
        if len(raw) > 1024 * 1024:
            raise HandoffError("Manifest is too large")
        manifest = json.loads(raw)
    except (ValueError, UnicodeError) as exc:
        raise HandoffError("Invalid manifest JSON") from exc
    if not isinstance(manifest, dict) or manifest.get("format") != FORMAT_VERSION:
        raise HandoffError("Unsupported manifest format")
    entries = manifest.get("files")
    if not isinstance(entries, dict) or DATABASE_NAME not in entries:
        raise HandoffError("Manifest lacks database entry")
    if set(names) != set(entries) | {MANIFEST_NAME}:
        raise HandoffError("Archive and manifest member lists differ")
    for name, value in entries.items():
        checked_member(name)
        if name != DATABASE_NAME and not name.startswith("media/"):
            raise HandoffError(f"Unexpected archive member: {name}")
        if not isinstance(value, dict) or set(value) != {"size", "sha256"}:
            raise HandoffError(f"Invalid manifest entry: {name}")
        digest = value["sha256"]
        if (
            type(value["size"]) is not int
            or value["size"] < 0
            or not isinstance(digest, str)
            or len(digest) != 64
            or any(c not in "0123456789abcdef" for c in digest)
        ):
            raise HandoffError(f"Invalid checksum or size: {name}")
    return entries


def extract_checked(archive_path: Path, destination: Path) -> int:
    """Validate every byte while extracting into a private, empty directory."""
    try:
        with zipfile.ZipFile(archive_path) as archive:
            entries = archive_entries(archive)
            (destination / "media").mkdir(exist_ok=True)
            for name, expected in entries.items():
                target = destination.joinpath(*name.split("/"))
                target.parent.mkdir(parents=True, exist_ok=True)
                with archive.open(name) as source, target.open("xb") as output:
                    size, digest = copy_and_hash(source, output)
                if size != expected["size"] or digest != expected["sha256"]:
                    raise HandoffError(f"Checksum mismatch: {name}")
        sqlite_integrity(destination / DATABASE_NAME)
        return len(entries) - 1
    except (zipfile.BadZipFile, EOFError, OSError) as exc:
        raise HandoffError(f"Cannot read archive: {exc}") from exc


def verify_archive(archive_path: Path) -> int:
    archive_path = archive_path.absolute()
    if not archive_path.is_file():
        raise HandoffError(f"Archive does not exist: {archive_path}")
    require_plain_path(archive_path)
    with tempfile.TemporaryDirectory(prefix="atlas-handoff-verify-") as scratch:
        return extract_checked(archive_path, Path(scratch))
