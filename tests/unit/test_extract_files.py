from pathlib import Path

from ingestion.extract_files import read_manifest
from ingestion.extract_files import sha256_of_file

def test_read_manifest_converts_paths_and_sizes(tmp_path: Path) -> None:
    # 1. ARRANGE: create a tiny fake manifest in a temporary folder
    manifest_file = tmp_path / "manifest.csv"
    manifest_file.write_text(
        "relative_path,file_size_bytes,sha256,created_at\n"
        "batch\\balances\\b_2026-01-01.csv,123,abc123,2026-07-23T08:26:13+00:00\n"
    )

    # 2. ACT: run the function
    result = read_manifest(manifest_file)

    # 3. ASSERT: check the result is what we expect
    key = "batch/balances/b_2026-01-01.csv"
    assert key in result
    assert result[key]["size"] == 123       
    assert result[key]["sha256"] == "abc123"        

def test_sha256_of_file_matches_known_value(tmp_path: Path) -> None:
    sample = tmp_path / "sample.txt"
    sample.write_bytes(b"hello")
    # This is the well-known sha256 of the word "hello"
    expected = "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
    assert sha256_of_file(sample) == expected


def test_sha256_is_same_with_tiny_chunks(tmp_path: Path) -> None:
    sample = tmp_path / "sample.txt"
    sample.write_bytes(b"hello")
    # Reading 2 bytes at a time must give the same fingerprint as reading it all at once
    assert sha256_of_file(sample, chunk_size=2) == sha256_of_file(sample)