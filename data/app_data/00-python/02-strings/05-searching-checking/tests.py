"""
pytest data/app_data/00-python/02-strings/05-searching-checking/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-python/02-strings/{Path(__file__).resolve().parent.name}")
find_all = _module.find_all
count_overlapping = _module.count_overlapping
has_extension = _module.has_extension
classify_token = _module.classify_token


def test_overlapping_matches_found():
    assert find_all("aaaa", "aa") == [0, 1, 2]


def test_no_matches_and_empty_substring():
    assert find_all("hello", "xyz") == []
    assert find_all("hello", "") == []
    assert count_overlapping("hello", "") == 0
    assert count_overlapping("aaaa", "aa") == 3


def test_has_extension_needs_a_real_dot():
    assert has_extension("Report.PDF", "pdf") is True
    assert has_extension("pdf", "pdf") is False
    assert has_extension("apdf", "pdf") is False


def test_classify_token_ordering():
    assert classify_token("123") == "digits"
    assert classify_token("abc123") == "alnum"
    assert classify_token("  ") == "space"
    assert classify_token("a-b") == "other"
    assert classify_token("") == "other"
    assert classify_token("abc") == "letters"


def test_search_does_not_misuse_negative_one():
    # Last character of "hello" is "o" -- searching for an absent
    # substring must not accidentally resolve via -1 indexing.
    assert find_all("hello", "z") == []
    assert has_extension("file.o", "xyz") is False
