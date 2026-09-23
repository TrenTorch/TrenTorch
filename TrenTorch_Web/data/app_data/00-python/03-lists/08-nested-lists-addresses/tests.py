"""
pytest data/app_data/00-python/03-lists/08-nested-lists-addresses/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-python/03-lists/{Path(__file__).resolve().parent.name}")
make_grid = _module.make_grid
rows_are_independent = _module.rows_are_independent
transpose = _module.transpose


def test_make_grid_rows_are_independent():
    grid = make_grid(2, 3, 0)
    grid[0].append(99)
    assert grid[1] == [0, 0, 0]


def test_make_grid_shapes():
    assert make_grid(0, 3, 0) == []
    assert make_grid(3, 0, 0) == [[], [], []]
    assert make_grid(1, 1, "x") == [["x"]]
    assert make_grid(2, 3, 0) == [[0, 0, 0], [0, 0, 0]]


def test_rows_are_independent_detects_the_star_trap():
    shared = [[0]] * 3
    assert rows_are_independent(shared) is False
    built = [[0] for _ in range(3)]
    assert rows_are_independent(built) is True
    assert rows_are_independent([]) is True
    assert rows_are_independent([[1]]) is True


def test_transpose_shape_values_and_non_square():
    result = transpose([[1, 2, 3], [4, 5, 6]])
    assert result == [[1, 4], [2, 5], [3, 6]]
    assert transpose([[1, 2, 3]]) == [[1], [2], [3]]


def test_transpose_does_not_share_rows_and_leaves_input_intact():
    matrix = [[1, 2, 3], [4, 5, 6]]
    result = transpose(matrix)
    result[0].append(99)
    assert matrix == [[1, 2, 3], [4, 5, 6]]
