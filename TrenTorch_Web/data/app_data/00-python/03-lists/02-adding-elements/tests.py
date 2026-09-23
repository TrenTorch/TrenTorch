"""
pytest data/app_data/00-python/03-lists/02-adding-elements/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-python/03-lists/{Path(__file__).resolve().parent.name}")
append_all = _module.append_all
insert_sorted = _module.insert_sorted
flatten_one_level = _module.flatten_one_level
concat_identity_report = _module.concat_identity_report


def test_append_all_adds_elements_not_nested_list():
    lst = [1, 2]
    result = append_all(lst, [3, 4])
    assert lst == [1, 2, 3, 4]
    assert result is None


def test_insert_sorted_position_and_stability():
    lst = [1, 3, 3, 5]
    insert_sorted(lst, 3)
    assert lst == [1, 3, 3, 3, 5]

    lst2 = [2, 4, 6]
    insert_sorted(lst2, 0)
    assert lst2 == [0, 2, 4, 6]
    insert_sorted(lst2, 100)
    assert lst2 == [0, 2, 4, 6, 100]

    lst3 = []
    insert_sorted(lst3, 5)
    assert lst3 == [5]


def test_flatten_one_level_independence():
    inner_a = [1, 2]
    inner_b = [3]
    original = [inner_a, inner_b]
    result = flatten_one_level(original)
    assert result == [1, 2, 3]
    assert original == [[1, 2], [3]]
    assert id(result) != id(inner_a)


def test_concat_identity_report_true_false():
    lst = [1, 2]
    result = concat_identity_report(lst, [3])
    assert result == [True, False]
    assert lst == [1, 2, 3]


def test_nothing_returned_by_in_place_functions():
    lst = [1, 3]
    assert insert_sorted(lst, 2) is None
