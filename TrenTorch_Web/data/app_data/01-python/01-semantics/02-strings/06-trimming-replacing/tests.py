"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
clean_field = _module.clean_field
remove_prefix_once = _module.remove_prefix_once
replace_first_n = _module.replace_first_n


def test_clean_field_step_order():
    assert clean_field("  a b.. ") == "a b"
    assert clean_field("  total ; ") == "total"


def test_remove_prefix_once_removes_exactly_one():
    assert remove_prefix_once("ababab", "ab") == "abab"


def test_prefix_absent_returns_unchanged():
    assert remove_prefix_once("hello", "xyz") == "hello"
    assert remove_prefix_once("ab", "abcdef") == "ab"


def test_replace_first_n_limits():
    assert replace_first_n("a-b-c-d", "-", "+", 0) == "a-b-c-d"
    assert replace_first_n("a-b-c-d", "-", "+", 1) == "a+b-c-d"
    assert replace_first_n("a-b-c-d", "-", "+", 100) == "a+b+c+d"
    assert replace_first_n("a-b-c-d", "-", "+", -1) == "a+b+c+d"


def test_original_unchanged():
    s = "  a b.. "
    clean_field(s)
    assert s == "  a b.. "
