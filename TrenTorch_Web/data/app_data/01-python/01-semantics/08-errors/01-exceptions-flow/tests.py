"""
pytest tests.py
"""

import pytest
from _load import load_solution

_module = load_solution(__file__)
validate_age = _module.validate_age
level_one = _module.level_one
first_element = _module.first_element


def test_validate_age_accepts_boundaries():
    assert validate_age(0) == 0
    assert validate_age(150) == 150
    assert validate_age(75) == 75


def test_validate_age_rejects_with_exact_message():
    with pytest.raises(ValueError, match="^age must be between 0 and 150$"):
        validate_age(-1)
    with pytest.raises(ValueError, match="^age must be between 0 and 150$"):
        validate_age(151)


def test_exception_propagates_through_the_chain():
    log = []
    with pytest.raises(RuntimeError, match="boom"):
        level_one(log)


def test_statements_after_raise_are_skipped():
    log = []
    try:
        level_one(log)
    except RuntimeError:
        pass
    assert log == ["L1 start", "L2 start", "L3 start"]


def test_first_element_raises_naturally():
    assert first_element([1, 2, 3]) == 1
    with pytest.raises(IndexError):
        first_element([])
