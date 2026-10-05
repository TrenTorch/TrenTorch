"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
make_singleton = _module.make_singleton
tuple_replace = _module.tuple_replace
count_and_first_index = _module.count_and_first_index
freeze_rows = _module.freeze_rows
thaw_rows = _module.thaw_rows
updated = _module.updated
has_mutable_element = _module.has_mutable_element


def test_make_singleton_produces_a_tuple():
    result = make_singleton(5)
    assert type(result) is tuple
    assert len(result) == 1
    assert result == (5,)
    result2 = make_singleton([1, 2])
    assert type(result2) is tuple
    assert len(result2) == 1


def test_tuple_replace_positions():
    assert tuple_replace((1, 2, 3), 0, 9) == (9, 2, 3)
    assert tuple_replace((1, 2, 3), 1, 9) == (1, 9, 3)
    assert tuple_replace((1, 2, 3), 2, 9) == (1, 2, 9)
    assert tuple_replace((1, 2, 3), -1, 9) == (1, 2, 9)


def test_tuple_replace_out_of_range_and_empty():
    assert tuple_replace((1, 2, 3), 3, 9) == (1, 2, 3)
    assert tuple_replace((1, 2, 3), -4, 9) == (1, 2, 3)
    assert tuple_replace((), 0, 9) == ()


def test_input_untouched_and_result_is_new():
    t = (1, 2, 3)
    before_id = id(t)
    result = tuple_replace(t, 0, 9)
    assert t == (1, 2, 3)
    assert id(t) == before_id
    assert id(result) != before_id


def test_count_and_first_index_absent_and_repeated():
    assert count_and_first_index((5, 3, 5), 5) == (2, 0)
    assert count_and_first_index((5, 3, 5), 9) == (0, -1)


def test_freeze_rows_types_at_both_levels():
    result = freeze_rows([[1, 2], [3]])
    assert type(result) is tuple
    assert all(type(row) is tuple for row in result)
    assert result == ((1, 2), (3,))


def test_thaw_rows_produces_independent_rows():
    frozen = ((1, 2), (3,))
    result = thaw_rows(frozen)
    result[0].append(99)
    assert frozen == ((1, 2), (3,))
    assert id(result[0]) != id(result[1])


def test_updated_preserves_input_type():
    lst = [1, 2, 3]
    result = updated(lst, 0, 9)
    assert type(result) is list
    assert result == [9, 2, 3]
    assert lst == [1, 2, 3]

    tup = (1, 2, 3)
    result2 = updated(tup, 0, 9)
    assert type(result2) is tuple
    assert result2 == (9, 2, 3)
    assert tup == (1, 2, 3)


def test_updated_out_of_range_index():
    lst = [1, 2, 3]
    result = updated(lst, 99, 9)
    assert result == [1, 2, 3]
    assert result is not lst


def test_has_mutable_element_all_kinds():
    assert has_mutable_element((1, [2])) is True
    assert has_mutable_element((1, {"a": 1})) is True
    assert has_mutable_element((1, {2, 3})) is True
    assert has_mutable_element((1, (2,))) is False
    assert has_mutable_element((1, "x", 2.5)) is False
