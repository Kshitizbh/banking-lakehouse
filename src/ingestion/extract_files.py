import csv
from pathlib import Path
import hashlib

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

def sha256_of_file(file_path: Path, chunk_size: int = 1024 * 1024) -> str:
    """
    Returns the SHA-256 fingerprint of a file as hex text, reading it in chunks.

    Args:
        file_path: Path to the file.
        chunk_size: Size of chunks to read at a time (default: 1MB).

    Returns:
        The SHA256 hash as a hexadecimal string.
    """
    digest = hashlib.sha256()
    with file_path.open("rb") as f:
        while chunk := f.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()