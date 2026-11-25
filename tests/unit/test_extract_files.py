from pathlib import Path

from ingestion.extract_files import read_manifest


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