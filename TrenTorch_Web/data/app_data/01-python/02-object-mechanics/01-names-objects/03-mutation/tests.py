"""
pytest tests.py
"""

import pytest
from _load import load_solution

_module = load_solution(__file__)
mutate_list = _module.mutate_list
reassign_list = _module.reassign_list
observe_through_alias = _module.observe_through_alias
is_mutable_type = _module.is_mutable_type
tuple_inner_mutation_check = _module.tuple_inner_mutation_check


def test_mutate_list_preserves_address():
    caller_list = [1, 2, 3]
    before = id(caller_list)
    mutate_list(caller_list)
    assert id(caller_list) == before
    assert caller_list == [1, 2, 3, 4]


def test_reassign_list_does_not_touch_input():
    original = [1, 2, 3]
    result = reassign_list(original)
    assert original == [1, 2, 3]
    assert result == [9, 9, 9]
    assert id(result) != id(original)


def test_alias_sees_mutation_but_not_reassignment():
    result = observe_through_alias([1, 2, 3])
    assert result["alias_after_mutation"] == [1, 2, 3, 100]
    assert result["alias_after_reassignment"] == [1, 2, 3, 100]


def test_original_final_reflects_only_the_reassignment():
    result = observe_through_alias([1, 2, 3])
    assert result["original_final"] == [0, 0, 0]


def test_correct_classification_across_built_in_types():
    assert is_mutable_type(1) is False
    assert is_mutable_type(1.5) is False
    assert is_mutable_type(True) is False
    assert is_mutable_type("hi") is False
    assert is_mutable_type((1, 2)) is False
    assert is_mutable_type(frozenset([1, 2])) is False
    assert is_mutable_type([1, 2]) is True
    assert is_mutable_type({"a": 1}) is True
    assert is_mutable_type({1, 2}) is True


def test_custom_object_instance_defaults_to_mutable():
    class Point:
        pass

    assert is_mutable_type(Point()) is True


def test_tuple_identity_preserved_through_inner_mutation():
    t = ([1, 2], "fixed")
    result = tuple_inner_mutation_check(t)
    assert result["tuple_id_before"] == result["tuple_id_after"]


def test_inner_list_actually_mutated():
    t = ([1, 2], "fixed")
    result = tuple_inner_mutation_check(t)
    assert result["inner_list_after"] == [1, 2, 100]


def test_reassigning_a_tuple_slot_raises_type_error():
    t = ([1, 2], "fixed")
    with pytest.raises(TypeError):
        t[0] = [9, 9]
