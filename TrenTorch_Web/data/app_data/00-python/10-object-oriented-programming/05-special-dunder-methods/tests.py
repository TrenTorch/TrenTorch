"""
pytest data/app_data/00-python/10-object-oriented-programming/05-special-dunder-methods/tests.py
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(
    f"00-python/10-object-oriented-programming/{Path(__file__).resolve().parent.name}"
)
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
