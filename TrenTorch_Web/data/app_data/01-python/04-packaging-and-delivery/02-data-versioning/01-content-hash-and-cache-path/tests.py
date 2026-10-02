"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
cache_path = _module.cache_path
content_hash = _module.content_hash


import hashlib


def test_known_digest():
    assert content_hash([b"hello"]) == "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"


def test_empty_input():
    assert content_hash([]) == hashlib.sha256(b"").hexdigest()


def test_chunking_does_not_change_the_hash():
    whole = content_hash([b"hello world"])
    assert content_hash([b"hello", b" ", b"world"]) == whole
    assert content_hash([b"h", b"ello wor", b"ld"]) == whole


def test_works_with_a_generator():
    def pieces():
        for i in range(3):
            yield bytes([65 + i]) * 4

    assert content_hash(pieces()) == hashlib.sha256(b"AAAABBBBCCCC").hexdigest()


def test_different_content_different_hash():
    assert content_hash([b"a"]) != content_hash([b"b"])


def test_cache_path_shards_on_first_two_characters():
    digest = "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
    path = cache_path(digest)
    assert path == "2c/" + digest[2:]
    assert path.replace("/", "") == digest
