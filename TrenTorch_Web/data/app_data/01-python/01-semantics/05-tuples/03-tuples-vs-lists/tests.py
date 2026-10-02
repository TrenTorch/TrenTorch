"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
freeze_rows = _module.freeze_rows
thaw_rows = _module.thaw_rows
updated = _module.updated
has_mutable_element = _module.has_mutable_element


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
