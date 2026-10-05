"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
describe_object = _module.describe_object
same_object = _module.same_object
chain_assign = _module.chain_assign


def test_type_correctness_across_categories():
    assert describe_object(1)["type"] == "int"
    assert describe_object(1.5)["type"] == "float"
    assert describe_object("hi")["type"] == "str"
    assert describe_object([1, 2])["type"] == "list"
    assert describe_object({"a": 1})["type"] == "dict"
    assert describe_object({1, 2})["type"] == "set"
    assert describe_object((1, 2))["type"] == "tuple"
    assert describe_object(True)["type"] == "bool"


def test_address_matches_id_directly():
    value = [1, 2, 3]
    assert describe_object(value)["address"] == id(value)


def test_different_objects_report_different_addresses():
    a = [1, 2, 3]
    b = [1, 2, 3]
    assert a == b
    assert describe_object(a)["address"] != describe_object(b)["address"]


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


def test_all_four_ids_identical():
    original = [1, 2, 3]
    result = chain_assign(original)
    assert result["a"] == result["b"] == result["c"] == result["original"]


def test_no_mutation_as_a_side_effect():
    original = [1, 2, 3]
    chain_assign(original)
    assert original == [1, 2, 3]


def test_works_for_non_list_objects_too():
    original = {"x": 1}
    result = chain_assign(original)
    assert result["a"] == result["b"] == result["c"] == result["original"]

    class Point:
        pass

    p = Point()
    result2 = chain_assign(p)
    assert result2["a"] == result2["b"] == result2["c"] == result2["original"]
