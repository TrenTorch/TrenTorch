"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
make_zero_grid = _module.make_zero_grid
make_filled_grid = _module.make_filled_grid
make_ones_vector = _module.make_ones_vector


def test_correct_shape_for_all_three_functions():
    assert make_zero_grid(3, 4).shape == (3, 4)
    assert make_filled_grid(2, 5, 9).shape == (2, 5)
    assert make_ones_vector(6).shape == (6,)


def test_correct_fill_values():
    assert np.all(make_zero_grid(2, 2) == 0)
    assert np.all(make_ones_vector(4) == 1)
    assert np.all(make_filled_grid(2, 2, 7) == 7)


def test_make_filled_grid_with_different_fill_value_types():
    assert np.all(make_filled_grid(2, 2, 3) == 3)
    assert np.all(make_filled_grid(2, 2, 2.5) == 2.5)
    assert np.all(make_filled_grid(2, 2, -4) == -4)


def test_single_row_and_single_column_edge_cases():
    row = make_zero_grid(1, 5)
    col = make_filled_grid(5, 1, 3)
    assert row.shape == (1, 5)
    assert col.shape == (5, 1)
