"""
pytest data/app_data/00-python/12-bridging-to-numpy-ml/05-assemble-vector-views/tests.py
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-python/12-bridging-to-numpy-ml/{Path(__file__).resolve().parent.name}")
Vector = _module.Vector


def test_slices_are_views():
    base = [0, 1, 2, 3, 4, 5]
    v = Vector(base)
    sliced = v[1:4]
    assert sliced.buffer is v.buffer
    sliced[0] = 99
    assert base[1] == 99
    assert v[1] == 99


def test_copy_and_map_are_independent():
    base = [1, 2, 3]
    v = Vector(base)
    c = v.copy()
    m = v.map(lambda x: x * 2)
    assert c.buffer is not base
    assert m.buffer is not base
    c[0] = 999
    m[0] = 999
    assert base == [1, 2, 3]


def test_slice_assignment_with_scalar_and_sequence():
    base = [0, 1, 2, 3, 4]
    v = Vector(base)
    v[1:3] = 0
    assert base == [0, 0, 0, 3, 4]

    base2 = [0, 1, 2, 3, 4]
    v2 = Vector(base2)
    v2[::2] = [9, 8, 7]
    assert base2 == [9, 1, 8, 3, 7]

    base3 = [0, 1, 2]
    v3 = Vector(base3)
    with pytest.raises(ValueError):
        v3[0:2] = [1, 2, 3]


def test_overlapping_slice_assignment():
    base = [1, 2, 3, 4]
    v = Vector(base)
    v[1:] = v[:-1]
    assert base == [1, 1, 2, 3]


def test_add_broadcasting_and_element_wise():
    v = Vector([1, 2, 3])
    r1 = v + 10
    assert r1.to_list() == [11, 12, 13]
    assert r1.buffer is not v.buffer

    r2 = v + [1, 1, 1]
    assert r2.to_list() == [2, 3, 4]

    w = Vector([10, 20, 30])
    r3 = v + w
    assert r3.to_list() == [11, 22, 33]
    assert v.to_list() == [1, 2, 3]
    assert w.to_list() == [10, 20, 30]


def test_sum_works_through_radd():
    v1 = Vector([1, 2])
    v2 = Vector([10, 20])
    v3 = Vector([100, 200])
    total = sum([v1, v2, v3])
    assert total.to_list() == [111, 222]

    base = [1, 2, 3, 4]
    partial = Vector(base, range(1, 3))
    result = sum([partial, Vector([100, 200])])
    assert result.to_list() == [102, 203]


def test_normalize_in_place_on_a_view():
    base = [0, 5, 10, 15, 0]
    v = Vector(base, range(1, 4))
    result = v.normalize_()
    assert result is v
    assert base[0] == 0
    assert base[4] == 0
    values = base[1:4]
    mean = sum(values) / len(values)
    assert abs(mean) < 1e-6

    Vector([]).normalize_()
    Vector([5, 5, 5]).normalize_()


def test_special_methods():
    v = Vector([1, 2, 3])
    assert len(v) == 3
    assert v[0] == 1
    assert v[-1] == 3
    with pytest.raises(IndexError):
        v[10]
    assert repr(v) == "Vector([1, 2, 3])"
    assert repr(v[1:]) == "Vector([2, 3])"
