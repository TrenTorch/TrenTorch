"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
append_all = _module.append_all
insert_sorted = _module.insert_sorted
flatten_one_level = _module.flatten_one_level
concat_identity_report = _module.concat_identity_report
remove_all = _module.remove_all
pop_last_n = _module.pop_last_n
delete_every_other = _module.delete_every_other
remove_first_or_report = _module.remove_first_or_report


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
