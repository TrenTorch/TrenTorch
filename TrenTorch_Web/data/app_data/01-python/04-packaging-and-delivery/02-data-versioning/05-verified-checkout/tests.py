"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
checkout = _module.checkout


import hashlib

import pytest


def sha(data):
    return hashlib.sha256(data).hexdigest()


def make(files):
    manifest = {path: sha(data) for path, data in files.items()}
    store = {sha(data): data for data in files.values()}
    return manifest, store


def test_restores_every_file():
    files = {"a.csv": b"1,2", "b/c.csv": b"3,4"}
    manifest, store = make(files)
    assert checkout(manifest, store) == files


def test_duplicate_content_shares_one_blob():
    files = {"x": b"same", "y": b"same"}
    manifest, store = make(files)
    assert len(store) == 1
    assert checkout(manifest, store) == files


def test_empty_manifest():
    assert checkout({}, {}) == {}


def test_missing_blob_raises_file_not_found():
    manifest, store = make({"a": b"1", "b": b"2"})
    del store[manifest["b"]]
    with pytest.raises(FileNotFoundError):
        checkout(manifest, store)


def test_corrupt_blob_raises_value_error():
    manifest, store = make({"a": b"1", "b": b"2"})
    store[manifest["a"]] = b"tampered"
    with pytest.raises(ValueError):
        checkout(manifest, store)


def test_missing_is_not_confused_with_corrupt():
    manifest = {"a": sha(b"1")}
    with pytest.raises(FileNotFoundError):
        checkout(manifest, {})
    with pytest.raises(ValueError):
        checkout(manifest, {sha(b"1"): b"nope"})
