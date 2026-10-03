"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
build_manifest = _module.build_manifest


import hashlib


def sha(data):
    return hashlib.sha256(data).hexdigest()


def test_entries_sorted_by_path_with_hashes():
    manifest = build_manifest({"b.csv": b"2", "a.csv": b"1"})
    assert manifest["entries"] == [
        {"path": "a.csv", "sha256": sha(b"1")},
        {"path": "b.csv", "sha256": sha(b"2")},
    ]


def test_counts_and_size():
    manifest = build_manifest({"a": b"123", "b": b"45", "c": b""})
    assert manifest["nfiles"] == 3
    assert manifest["size"] == 5


def test_digest_matches_the_defined_text_form():
    manifest = build_manifest({"b": b"2", "a": b"1"})
    text = f"a\t{sha(b'1')}\nb\t{sha(b'2')}"
    assert manifest["digest"] == sha(text.encode("utf-8"))


def test_insertion_order_does_not_matter():
    one = build_manifest({"a": b"1", "b": b"2", "c": b"3"})
    two = build_manifest({"c": b"3", "a": b"1", "b": b"2"})
    assert one["digest"] == two["digest"]


def test_content_change_changes_digest():
    assert build_manifest({"a": b"1"})["digest"] != build_manifest({"a": b"2"})["digest"]


def test_rename_changes_digest_even_with_same_bytes():
    assert build_manifest({"a": b"1"})["digest"] != build_manifest({"z": b"1"})["digest"]


def test_empty_directory():
    manifest = build_manifest({})
    assert manifest["entries"] == []
    assert manifest["nfiles"] == 0
    assert manifest["size"] == 0
    assert manifest["digest"] == sha(b"")
