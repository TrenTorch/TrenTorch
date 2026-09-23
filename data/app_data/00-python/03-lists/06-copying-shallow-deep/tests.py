"""
pytest data/app_data/00-python/03-lists/06-copying-shallow-deep/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-python/03-lists/{Path(__file__).resolve().parent.name}")
shallow_copy = _module.shallow_copy
deep_copy = _module.deep_copy
shares_inner_objects = _module.shares_inner_objects
add_row_safely = _module.add_row_safely


def test_shallow_copy_new_list_shares_elements():
    a = [[1, 2], [3]]
    b = shallow_copy(a)
    assert id(b) != id(a)
    b.append([4])
    assert a == [[1, 2], [3]]
    assert shares_inner_objects(a, shallow_copy(a)) is True


def test_shallow_copy_shows_shared_mutation():
    a = [[1, 2], [3]]
    b = shallow_copy(a)
    b[0].append(99)
    assert a == [[1, 2, 99], [3]]


def test_deep_copy_independence_at_depth():
    a = [[1, [2, 3]], [4]]
    b = deep_copy(a)
    b[0][1].append(99)
    assert a == [[1, [2, 3]], [4]]


def test_shares_inner_objects_distinguishes_equal_from_identical():
    a = [[1, 2], [3]]
    b = deep_copy(a)
    assert shares_inner_objects(a, b) is False
    assert shares_inner_objects([], []) is True


def test_add_row_safely_leaves_every_input_untouched():
    matrix = [[1, 2], [3, 4]]
    row = [5, 6]
    result = add_row_safely(matrix, row)
    assert result == [[1, 2], [3, 4], [5, 6]]

    result[0].append(99)
    result[2].append(7)
    assert matrix == [[1, 2], [3, 4]]
    assert row == [5, 6]
