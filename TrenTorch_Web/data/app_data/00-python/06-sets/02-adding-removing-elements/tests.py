"""
pytest data/app_data/00-python/06-sets/02-adding-removing-elements/tests.py
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-python/06-sets/{Path(__file__).resolve().parent.name}")
add_values = _module.add_values
remove_if_present = _module.remove_if_present
remove_required = _module.remove_required
empty_set = _module.empty_set


def test_add_uniqueness():
    original = {1, 2}
    result = add_values(original, [2, 3, 4])
    assert result == {1, 2, 3, 4}
    assert original == {1, 2}


def test_discard_absent_value():
    s = {1, 2, 3}
    result = remove_if_present(s, 99)
    assert result == {1, 2, 3}


def test_remove_absent_value_raises():
    s = {1, 2}
    with pytest.raises(KeyError):
        remove_required(s, 99)


def test_mutation_and_identity():
    s = {1, 2, 3}
    result = remove_if_present(s, 2)
    assert result is s
    assert s == {1, 3}

    s2 = {1, 2, 3}
    result2 = remove_required(s2, 2)
    assert result2 is s2


def test_clear():
    s = {1, 2, 3}
    result = empty_set(s)
    assert result == set()
    assert result is s
