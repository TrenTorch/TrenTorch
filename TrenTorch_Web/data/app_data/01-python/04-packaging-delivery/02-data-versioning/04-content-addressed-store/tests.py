"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
dedupe_stats = _module.dedupe_stats
store_put = _module.store_put


import hashlib


def test_put_returns_the_sha256_digest_and_stores_the_bytes():
    store = {}
    digest = store_put(store, b"hello")
    assert digest == hashlib.sha256(b"hello").hexdigest()
    assert store == {digest: b"hello"}


def test_same_content_is_stored_once():
    store = {}
    first = store_put(store, b"data")
    second = store_put(store, b"data")
    assert first == second
    assert len(store) == 1


def test_different_content_gets_different_keys():
    store = {}
    a = store_put(store, b"a")
    b = store_put(store, b"b")
    assert a != b and len(store) == 2


def test_existing_entry_is_left_alone():
    sentinel = b"original"
    digest = hashlib.sha256(b"x").hexdigest()
    store = {digest: sentinel}
    store_put(store, b"x")
    assert store[digest] is sentinel


def test_dedupe_stats_with_duplicates():
    stats = dedupe_stats([b"aaaa", b"bb", b"aaaa", b"aaaa", b"bb"])
    assert stats == {"total_bytes": 16, "stored_bytes": 6, "unique": 2}


def test_dedupe_stats_without_duplicates():
    assert dedupe_stats([b"a", b"bc", b"def"]) == {"total_bytes": 6, "stored_bytes": 6, "unique": 3}


def test_dedupe_stats_empty():
    assert dedupe_stats([]) == {"total_bytes": 0, "stored_bytes": 0, "unique": 0}
