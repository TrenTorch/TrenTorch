"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

extra_tree_split = load_solution(__file__).extra_tree_split


def _raises_value_error(function, *args, **kwargs):
    try:
        function(*args, **kwargs)
    except ValueError:
        return True
    return False


def _x():
    return np.array([0.0, 1.0, 2.0, 8.0, 9.0, 10.0])


def _y():
    return np.array([0, 0, 0, 1, 1, 1])


def test_threshold_is_the_seeded_uniform_draw():
    thr, _ = extra_tree_split(_x(), _y(), seed=4)
    expected = np.random.default_rng(4).uniform(0.0, 10.0)
    assert np.isclose(thr, expected)


def test_threshold_stays_inside_the_feature_range():
    for seed in range(30):
        thr, _ = extra_tree_split(_x(), _y(), seed)
        assert 0.0 <= thr <= 10.0


def test_gain_is_full_when_threshold_separates_the_classes():
    for seed in range(50):
        thr, gain = extra_tree_split(_x(), _y(), seed)
        if 2.0 < thr < 8.0:
            assert np.isclose(gain, 0.5)
            return
    raise AssertionError("no seed in range produced a separating threshold")


def test_gain_is_below_full_when_threshold_splits_a_class():
    for seed in range(50):
        thr, gain = extra_tree_split(_x(), _y(), seed)
        if not 2.0 < thr < 8.0:
            assert gain < 0.5
            return
    raise AssertionError("no seed in range produced a non-separating threshold")


def test_gain_is_never_negative():
    for seed in range(40):
        _, gain = extra_tree_split(_x(), _y(), seed)
        assert gain >= -1e-12


def test_constant_feature_returns_none():
    thr, gain = extra_tree_split(np.ones(5), np.array([0, 1, 0, 1, 0]), seed=0)
    assert thr is None
    assert gain == 0.0


def test_pure_labels_give_zero_gain():
    _, gain = extra_tree_split(_x(), np.zeros(6, dtype=int), seed=3)
    assert gain == 0.0


def test_empty_side_gives_zero_gain():
    x = np.array([5.0, 5.0, 5.0, 5.0])
    thr, gain = extra_tree_split(x, np.array([0, 1, 0, 1]), seed=1)
    assert thr is None
    assert gain == 0.0


def test_length_mismatch_raises():
    assert _raises_value_error(extra_tree_split, _x(), np.array([0, 1]), 0)


def test_same_seed_gives_same_split():
    assert extra_tree_split(_x(), _y(), 9) == extra_tree_split(_x(), _y(), 9)


def test_does_not_modify_inputs():
    x = _x()
    y = _y()
    x0, y0 = x.copy(), y.copy()
    extra_tree_split(x, y, 2)
    assert np.array_equal(x, x0) and np.array_equal(y, y0)
