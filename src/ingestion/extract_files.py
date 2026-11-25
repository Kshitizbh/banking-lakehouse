import csv
from pathlib import Path

def read_manifest(manifest_path: Path) -> dict[str, dict]:
    """
    Reads the sender's manifest into a lookup.

    Returns {relative_path: {"size": int, "sha256": str}}
    Windows backslashes in paths are converted to forward slashes.
    """
    manifest: dict[str, dict] = {}
    with manifest_path.open(newline="") as f:
        for row in csv.DictReader(f):
            path = row["relative_path"].replace("\\", "/")
            manifest[path] = {
                "size": int(row["file_size_bytes"]),
                "sha256": row["sha256"],
            }
    return manifest