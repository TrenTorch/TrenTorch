"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
verify_artifact = _module.verify_artifact


import hashlib

HELLO_SHA256 = "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"


def test_matching_hash_passes():
    assert verify_artifact(b"hello", [f"sha256:{HELLO_SHA256}"]) is True


def test_mismatching_hash_fails():
    assert verify_artifact(b"hello!", [f"sha256:{HELLO_SHA256}"]) is False


def test_any_of_multiple_hashes_is_enough():
    other = hashlib.sha256(b"other-platform-wheel").hexdigest()
    assert verify_artifact(b"hello", [f"sha256:{other}", f"sha256:{HELLO_SHA256}"]) is True


def test_uppercase_hex_accepted():
    assert verify_artifact(b"hello", [f"sha256:{HELLO_SHA256.upper()}"]) is True


def test_other_algorithms():
    sha512 = hashlib.sha512(b"data").hexdigest()
    assert verify_artifact(b"data", [f"sha512:{sha512}"]) is True


def test_empty_allowed_list_rejects():
    assert verify_artifact(b"hello", []) is False


def test_unsupported_algorithm_raises():
    try:
        verify_artifact(b"hello", ["md5:5d41402abc4b2a76b9719d911017c592"])
    except ValueError:
        return
    raise AssertionError("md5 should be rejected")


def test_malformed_entry_raises_even_after_a_match():
    try:
        verify_artifact(b"hello", [f"sha256:{HELLO_SHA256}", "not-a-hash"])
    except ValueError:
        return
    raise AssertionError("a malformed entry must raise, even when an earlier one matches")
