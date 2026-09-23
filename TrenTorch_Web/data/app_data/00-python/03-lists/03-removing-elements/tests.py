"""
pytest data/app_data/00-python/03-lists/03-removing-elements/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-python/03-lists/{Path(__file__).resolve().parent.name}")
remove_all = _module.remove_all
pop_last_n = _module.pop_last_n
delete_every_other = _module.delete_every_other
remove_first_or_report = _module.remove_first_or_report


def test_remove_all_consecutive_duplicates():
    lst = [1, 1, 1, 2]
    remove_all(lst, 1)
    assert lst == [2]

    lst2 = [2, 1, 1]
    remove_all(lst2, 1)
    assert lst2 == [2]


def test_remove_all_keeps_same_list_object():
    lst = [1, 1, 2, 1]
    before_id = id(lst)
    alias = lst
    remove_all(lst, 1)
    assert id(lst) == before_id
    assert alias == [2]


def test_pop_last_n_order_and_bounds():
    lst = [1, 2, 3, 4]
    assert pop_last_n(lst, 2) == [3, 4]
    assert lst == [1, 2]

    lst2 = [1, 2, 3]
    assert pop_last_n(lst2, 0) == []
    assert lst2 == [1, 2, 3]
    assert pop_last_n(lst2, -5) == []
    assert lst2 == [1, 2, 3]

    lst3 = [1, 2, 3]
    assert pop_last_n(lst3, 3) == [1, 2, 3]
    assert lst3 == []

    lst4 = [1, 2]
    assert pop_last_n(lst4, 10) == [1, 2]
    assert lst4 == []


def test_delete_every_other_various_lengths():
    lst = [1, 2, 3, 4, 5]
    delete_every_other(lst)
    assert lst == [2, 4]

    lst2 = [1, 2, 3, 4]
    delete_every_other(lst2)
    assert lst2 == [2, 4]

    lst3 = []
    delete_every_other(lst3)
    assert lst3 == []

    lst4 = [1]
    delete_every_other(lst4)
    assert lst4 == []


def test_remove_first_or_report_only_first_match():
    lst = [1, 2, 1, 2]
    assert remove_first_or_report(lst, 2) is True
    assert lst == [1, 1, 2]

    lst2 = [1, 2]
    assert remove_first_or_report(lst2, 99) is False
    assert lst2 == [1, 2]
