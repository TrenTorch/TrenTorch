"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
same_object = _module.same_object


def test_same_variable_value_is_same_object():
    x = [1, 2, 3]
    y = x
    assert same_object(x, y) is True


def test_equal_value_different_object_is_false():
    x = [1, 2, 3]
    y = [1, 2, 3]
    assert x == y
    assert same_object(x, y) is False


def test_different_values_entirely_is_false():
    assert same_object([1, 2, 3], "hello") is False
    assert same_object(1, 2) is False
