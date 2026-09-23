"""
pytest data/app_data/00-python/01-core-semantics/08-identity-vs-equality/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-python/01-core-semantics/{Path(__file__).resolve().parent.name}")
classify_pair = _module.classify_pair


def test_same_object_reference_is_identical():
    x = [1, 2, 3]
    assert classify_pair(x, x) == "identical"


def test_separately_built_equal_valued_objects():
    a = [1, 2, 3]
    b = [1, 2, 3]
    assert classify_pair(a, b) == "equal_not_identical"

    c = {"x": 1}
    d = {"x": 1}
    assert classify_pair(c, d) == "equal_not_identical"


def test_different_values_entirely_are_not_equal():
    assert classify_pair([1, 2], [3, 4]) == "not_equal"
    assert classify_pair("abc", "xyz") == "not_equal"


def test_none_comparisons():
    assert classify_pair(None, None) == "identical"
    assert classify_pair(5, None) == "not_equal"
    assert classify_pair(None, 5) == "not_equal"
