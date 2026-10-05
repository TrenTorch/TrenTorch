"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
oblique_split_gain = _module.oblique_split_gain


def _raises_value_error(function, *args, **kwargs):
    try:
        function(*args, **kwargs)
    except ValueError:
        return True
    return False


X_DIAGONAL = np.array([[0.0, 2.0], [1.0, 3.0], [2.0, 0.0], [3.0, 1.0]])
Y_DIAGONAL = np.array([0, 0, 1, 1])


def test_diagonal_boundary_is_separated_by_one_oblique_split():
    # x0 - x1 is -2, -2, 2, 2, so the sign separates the two classes perfectly.
    gain = oblique_split_gain(X_DIAGONAL, Y_DIAGONAL, [1.0, -1.0], 0.0)
    assert np.isclose(gain, 0.5)


def test_axis_aligned_split_matches_gini_gain_on_one_feature():
    X = np.array([[1.0], [2.0], [8.0], [9.0]])
    gain = oblique_split_gain(X, [0, 0, 1, 1], [1.0], -5.0)
    assert np.isclose(gain, 0.5)


def test_scaling_w_and_b_together_does_not_change_gain():
    base = oblique_split_gain(X_DIAGONAL, Y_DIAGONAL, [1.0, -1.0], 0.5)
    scaled = oblique_split_gain(X_DIAGONAL, Y_DIAGONAL, [3.0, -3.0], 1.5)
    assert np.isclose(base, scaled)


def test_split_that_sends_every_row_left_has_zero_gain():
    gain = oblique_split_gain(X_DIAGONAL, Y_DIAGONAL, [1.0, -1.0], -10.0)
    assert np.isclose(gain, 0.0)


def test_pure_parent_has_zero_gain():
    gain = oblique_split_gain(X_DIAGONAL, [1, 1, 1, 1], [1.0, -1.0], 0.0)
    assert np.isclose(gain, 0.0)


def test_gain_is_never_negative_on_random_data():
    rng = np.random.default_rng(1)
    for _ in range(20):
        X = rng.normal(size=(25, 3))
        y = rng.integers(0, 2, size=25)
        w = rng.normal(size=3)
        assert oblique_split_gain(X, y, w, 0.0) >= -1e-12


def test_gain_is_at_most_the_parent_impurity():
    rng = np.random.default_rng(2)
    X = rng.normal(size=(30, 2))
    y = rng.integers(0, 2, size=30)
    p = y.mean()
    parent = 1 - p ** 2 - (1 - p) ** 2
    assert oblique_split_gain(X, y, [0.3, -0.8], 0.1) <= parent + 1e-12


def test_gain_does_not_depend_on_label_names():
    base = oblique_split_gain(X_DIAGONAL, Y_DIAGONAL, [1.0, -1.0], 0.0)
    renamed = oblique_split_gain(X_DIAGONAL, np.array([4, 4, 9, 9]), [1.0, -1.0], 0.0)
    assert np.isclose(base, renamed)


def test_zero_direction_raises():
    assert _raises_value_error(oblique_split_gain, X_DIAGONAL, Y_DIAGONAL, [0.0, 0.0], 0.0)


def test_weight_length_mismatch_raises():
    assert _raises_value_error(oblique_split_gain, X_DIAGONAL, Y_DIAGONAL, [1.0], 0.0)


def test_label_length_mismatch_raises():
    assert _raises_value_error(oblique_split_gain, X_DIAGONAL, [0, 1], [1.0, -1.0], 0.0)


def test_inputs_are_not_modified():
    X = X_DIAGONAL.copy()
    y = Y_DIAGONAL.copy()
    w = np.array([1.0, -1.0])
    oblique_split_gain(X, y, w, 0.0)
    assert np.array_equal(X, X_DIAGONAL) and np.array_equal(y, Y_DIAGONAL)
