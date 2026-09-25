"""
pytest data/app_data/00-python/12-bridging-to-numpy-ml/02-views-vs-copies/tests.py
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-python/12-bridging-to-numpy-ml/{Path(__file__).resolve().parent.name}")
View = _module.View
shares_buffer = _module.shares_buffer
scale_in_place = _module.scale_in_place
scaled_copy = _module.scaled_copy


def test_writes_through_view_reach_the_buffer():
    base = [0, 1, 2, 3, 4, 5]
    v = View(base)
    other = View(base)
    v[0] = 99
    assert base[0] == 99
    assert other[0] == 99


def test_slicing_a_view_yields_a_view_not_a_copy():
    base = [0, 1, 2, 3, 4, 5]
    v = View(base)
    sliced = v[1:4]
    assert isinstance(sliced, View)
    assert shares_buffer(v, sliced) is True
    sliced[0] = 100
    assert base[1] == 100


def test_slices_of_slices_and_steps():
    base = list(range(10))
    v = View(base)
    stepped = v[::2]
    assert stepped.to_list() == [0, 2, 4, 6, 8]
    further = stepped[1:]
    assert further.to_list() == [2, 4, 6, 8]
    assert further[-1] == 8


def test_to_list_and_scaled_copy_are_independent():
    base = [1, 2, 3]
    v = View(base)
    lst = v.to_list()
    lst.append(99)
    assert base == [1, 2, 3]

    copy = scaled_copy(v, 10)
    copy.append(99)
    assert base == [1, 2, 3]


def test_scale_in_place_mutates_buffer_only_at_exposed_positions():
    base = [1, 2, 3, 4, 5]
    v = View(base, range(1, 4))
    before_id = id(base)
    scale_in_place(v, 10)
    assert base == [1, 20, 30, 40, 5]
    assert id(base) == before_id


def test_bounds():
    base = [1, 2, 3]
    v = View(base)
    with pytest.raises(IndexError):
        v[10]
    empty = v[3:3]
    assert len(empty) == 0
