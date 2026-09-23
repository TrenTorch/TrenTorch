"""
pytest data/app_data/00-python/01-core-semantics/13-truthy-falsy/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-python/01-core-semantics/{Path(__file__).resolve().parent.name}")
is_truthy = _module.is_truthy
first_truthy = _module.first_truthy


def test_all_documented_falsy_values():
    assert is_truthy(False) is False
    assert is_truthy(None) is False
    assert is_truthy(0) is False
    assert is_truthy(0.0) is False
    assert is_truthy("") is False
    assert is_truthy([]) is False
    assert is_truthy(()) is False
    assert is_truthy({}) is False
    assert is_truthy(set()) is False


def test_non_empty_non_zero_values_are_truthy():
    assert is_truthy("0") is True
    assert is_truthy("False") is True
    assert is_truthy([0]) is True
    assert is_truthy((0,)) is True
    assert is_truthy({"a": 1}) is True
    assert is_truthy(-5) is True
    assert is_truthy(1) is True
    assert is_truthy(True) is True


def test_first_truthy_skips_leading_falsy_values():
    assert first_truthy([0, "", None, "found", 5]) == "found"


def test_first_truthy_returns_none_when_nothing_is_truthy():
    assert first_truthy([0, "", None, [], {}]) is None
