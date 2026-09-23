"""
pytest data/app_data/00-python/03-lists/07-list-comprehensions/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-python/03-lists/{Path(__file__).resolve().parent.name}")
squares_of_evens = _module.squares_of_evens
label_parity = _module.label_parity
flatten = _module.flatten
multiplication_table = _module.multiplication_table


def test_filter_versus_value_choice():
    numbers = [1, 2, 3, 4]
    assert squares_of_evens(numbers) == [4, 16]
    assert len(label_parity(numbers)) == len(numbers)


def test_negative_and_zero_values():
    assert squares_of_evens([-2, -1, 0]) == [4, 0]
    assert label_parity([-2, -1, 0]) == ["even", "odd", "even"]


def test_flatten_empty_inner_and_outer():
    assert flatten([]) == []
    assert flatten([[], []]) == []
    assert flatten([[1, 2], [], [3]]) == [1, 2, 3]


def test_multiplication_table_shape_and_independence():
    table = multiplication_table(2)
    assert table == [[1, 2], [2, 4]]
    assert id(table[0]) != id(table[1])
    assert multiplication_table(0) == []
    assert multiplication_table(-1) == []


def test_input_untouched():
    numbers = [1, 2, 3, 4]
    squares_of_evens(numbers)
    label_parity(numbers)
    assert numbers == [1, 2, 3, 4]

    nested = [[1, 2], [3]]
    flatten(nested)
    assert nested == [[1, 2], [3]]
