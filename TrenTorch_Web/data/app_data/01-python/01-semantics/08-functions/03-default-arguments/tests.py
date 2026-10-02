"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
power = _module.power
make_label = _module.make_label
append_value = _module.append_value
describe_config = _module.describe_config


def test_default_usage():
    assert power(5) == 25
    assert make_label(7) == "item:7"
    assert describe_config("server") == ("server", True, 3)


def test_explicit_override():
    assert power(2, 3) == 8
    assert make_label(7, "id") == "id:7"
    assert describe_config("server", False, 5) == ("server", False, 5)


def test_default_binding_not_affected_by_external_reassignment():
    x = 10

    def show(value=x):
        return value

    x = 20
    assert show() == 10


def test_fresh_mutable_default_behavior():
    result1 = append_value(1)
    result2 = append_value(2)
    assert result1 == [1]
    assert result2 == [2]


def test_supplied_mutable_object_is_mutated_and_returned():
    xs = [10]
    result = append_value(20, xs)
    assert xs == [10, 20]
    assert result is xs
