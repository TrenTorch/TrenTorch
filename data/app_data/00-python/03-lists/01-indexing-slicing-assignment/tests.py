"""
pytest data/app_data/00-python/03-lists/01-indexing-slicing-assignment/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-python/03-lists/{Path(__file__).resolve().parent.name}")
replace_middle = _module.replace_middle
set_every_other = _module.set_every_other
slice_copy = _module.slice_copy


def test_replace_middle_mutates_in_place():
    lst = [1, 2, 3, 4]
    before_id = id(lst)
    replace_middle(lst, ["x"])
    assert lst == [1, "x", 4]
    assert id(lst) == before_id


def test_replace_middle_lengths():
    lst = [1, 2, 3, 4]
    replace_middle(lst, [])
    assert lst == [1, 4]

    lst2 = [1, 2]
    replace_middle(lst2, ["a", "b"])
    assert lst2 == [1, "a", "b", 2]

    lst3 = [1]
    replace_middle(lst3, ["a"])
    assert lst3 == [1]

    lst4 = []
    replace_middle(lst4, ["a"])
    assert lst4 == []


def test_set_every_other_odd_and_even_lengths():
    lst = [1, 2, 3, 4, 5]
    set_every_other(lst, 0)
    assert lst == [0, 2, 0, 4, 0]

    lst2 = [1, 2, 3, 4]
    set_every_other(lst2, 9)
    assert lst2 == [9, 2, 9, 4]

    lst3 = [1]
    set_every_other(lst3, 9)
    assert lst3 == [9]

    lst4 = []
    set_every_other(lst4, 9)
    assert lst4 == []


def test_slice_copy_shared_elements_and_bounds():
    lst = [10, 20, 30, 40, 50]
    result = slice_copy(lst, 1, 3)
    assert result == [20, 30]
    assert id(result) != id(lst)
    assert slice_copy(lst, -2, 100) == [40, 50]
    assert lst == [10, 20, 30, 40, 50]
