"""
pytest tests.py
"""

import pytest

from _load import load_solution

_module = load_solution(__file__)
Vec = _module.Vec


def test_repr_format():
    assert repr(Vec(1, 2, 3)) == "Vec(1, 2, 3)"
    assert repr(Vec()) == "Vec()"
    assert repr(Vec(-1, 2.5)) == "Vec(-1, 2.5)"


def test_print_and_str_use_repr():
    assert str(Vec(1)) == repr(Vec(1))


def test_eq_value_equality_and_foreign_types():
    assert Vec(1, 2) == Vec(1, 2)
    assert Vec(1, 2) != Vec(2, 1)
    assert (Vec(1) == [1]) is False
    assert Vec(1).__eq__([1]) is NotImplemented


def test_len_truthiness_and_iteration():
    assert len(Vec(1, 2, 3)) == 3
    assert bool(Vec()) is False
    assert list(Vec(1, 2, 3)) == [1, 2, 3]


def test_indexing_and_slicing():
    v = Vec(1, 2, 3)
    assert v[0] == 1
    assert v[-1] == 3
    sliced = v[1:]
    assert isinstance(sliced, Vec)
    assert sliced == Vec(2, 3)
    with pytest.raises(IndexError):
        v[10]


def test_independence_of_stored_data():
    v = Vec(1, 2, 3)
    sliced = v[1:]
    sliced.data.append(99)
    assert v.data == [1, 2, 3]
