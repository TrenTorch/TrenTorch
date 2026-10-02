"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
did_mutate_in_place = _module.did_mutate_in_place
are_same_object = _module.are_same_object
classify_pair = _module.classify_pair


def test_in_place_methods_detected_correctly():
    assert did_mutate_in_place([1, 2], lambda l: l.append(99)) is True
    assert did_mutate_in_place([1, 2], lambda l: l.extend([3, 4])) is True
    assert did_mutate_in_place([3, 1, 2], lambda l: l.sort()) is True


def test_reassignment_style_operation_detected_correctly():
    assert did_mutate_in_place([1, 2], lambda l: l + [99]) is False


def test_are_same_object_diverges_from_equals():
    a = [1, 2, 3]
    b = [1, 2, 3]
    assert a == b
    assert are_same_object(a, b) is False


def test_are_same_object_on_identical_reference():
    a = [1, 2, 3]
    assert are_same_object(a, a) is True


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
