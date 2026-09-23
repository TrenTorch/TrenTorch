"""
pytest data/app_data/00-python/01-core-semantics/09-mutable-vs-immutable-types/tests.py
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-python/01-core-semantics/{Path(__file__).resolve().parent.name}")
is_mutable_type = _module.is_mutable_type
tuple_inner_mutation_check = _module.tuple_inner_mutation_check


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
