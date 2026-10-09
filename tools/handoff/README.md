# Offline Atlas handoff archive

This small Python 3.13+ standard library tool packages a **SQLite snapshot and the complete media directory** into one ZIP file. It does not load Django settings, read `.env`, contact Syncthing, or schedule backups. Use explicit paths from the computer holding the data; do not point the example commands at the repository's sample or development data unless those are the files you intend to transfer.

Before creating an archive, stop every process that can write the database or media (web server, worker, editor, and file copying). The SQLite backup API makes a consistent database snapshot, but it cannot coordinate a photo being changed during copying. `--writers-stopped` records the operator's acknowledgement; the tool cannot prove writers stopped.

From the repository root in PowerShell, create **two existing directories** on the same filesystem: a private staging directory outside the Syncthing folder and a finished-archive directory that Syncthing may sync. The output filename must be new. Paths may be absolute or relative to the current directory; do not use `..` parent segments. For example, after substituting your own paths:

```powershell
python -B -m tools.handoff create `
  --database 'D:\AtlasData\db.sqlite3' `
  --media 'D:\AtlasData\media' `
  --staging 'D:\AtlasPrivateStaging' `
  --output 'D:\AtlasFinishedArchives\atlas-2026-10-09.zip' `
  --writers-stopped
```

The tool writes its temporary SQLite snapshot and ZIP in staging, verifies all checksums and SQLite integrity, then renames the completed ZIP into the output directory. Staging and output must be on the same filesystem so that publication is atomic. An existing output is never replaced. Files named `.env` or `.env.*`, links, and Windows reparse points in the source are rejected. The archive contains the SQLite snapshot and regular media files; an empty media directory is recreated on restore.

On the receiving computer, verify the completed archive, then restore it to a **new path that does not exist yet**:

```powershell
python -B -m tools.handoff verify 'D:\AtlasFinishedArchives\atlas-2026-10-09.zip'
python -B -m tools.handoff restore 'D:\AtlasFinishedArchives\atlas-2026-10-09.zip' `
  --target 'D:\AtlasRestored\incoming-2026-10-09'
```

The target will contain `database.sqlite3` and `media/`. Restore validates the ZIP member names, checksums, and SQLite integrity in a private temporary directory beside the target, then publishes the complete directory. It refuses an existing target, including an empty one. The tool does not modify the original database or media and does not put the restored files into a live Django installation. Keep completed archive files immutable; make a new filename for each handoff.

Run the synthetic tests without a Django environment:

```powershell
python -B -m unittest discover -s tools\handoff\tests -v
```
