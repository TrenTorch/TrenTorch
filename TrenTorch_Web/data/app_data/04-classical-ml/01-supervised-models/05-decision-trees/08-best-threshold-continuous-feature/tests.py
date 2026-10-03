"""
pytest tests.py
"""

import math

import numpy as np

from _load import load_solution

best_threshold = load_solution(__file__).best_threshold


def _h(labels):
    labels = list(labels)
    if not labels:
        return 0.0
    n = len(labels)
    return -sum((labels.count(c) / n) * math.log2(labels.count(c) / n) for c in set(labels))


def test_perfectly_separable_data():
    x = np.array([1.0, 2.0, 3.0, 10.0, 11.0, 12.0])
    y = np.array([0, 0, 0, 1, 1, 1])
    t, gain = best_threshold(x, y)
    assert np.isclose(t, 6.5)
    assert np.isclose(gain, 1.0)


def test_input_order_does_not_matter():
    x = np.array([12.0, 1.0, 11.0, 2.0, 10.0, 3.0])
    y = np.array([1, 0, 1, 0, 1, 0])
    t, gain = best_threshold(x, y)
    assert np.isclose(t, 6.5)
    assert np.isclose(gain, 1.0)


def test_constant_feature_returns_none():
    assert best_threshold(np.array([5.0, 5.0, 5.0]), np.array([0, 1, 0])) == (None, 0.0)


def test_threshold_is_never_an_observed_value():
    rng = np.random.default_rng(3)
    x = rng.integers(0, 20, size=40).astype(float)
    y = rng.integers(0, 2, size=40)
    t, _ = best_threshold(x, y)
    assert t not in set(x.tolist())


def test_matches_brute_force_search():
    rng = np.random.default_rng(1)
    for _ in range(5):
        x = np.round(rng.normal(size=30), 1)
        y = rng.integers(0, 3, size=30)
        values = sorted(set(x.tolist()))
        best = (None, -1.0)
        for a, b in zip(values, values[1:]):
            t = (a + b) / 2
            left = [lab for xi, lab in zip(x, y) if xi <= t]
            right = [lab for xi, lab in zip(x, y) if xi > t]
            gain = _h(y) - (len(left) * _h(left) + len(right) * _h(right)) / len(y)
            if gain > best[1] + 1e-12:
                best = (t, gain)
        t, gain = best_threshold(x, y)
        assert np.isclose(t, best[0])
        assert np.isclose(gain, best[1])


def test_ties_return_smallest_threshold():
    # Two equally good, mirror-image cut points exist: pick the smaller.
    x = np.array([1.0, 2.0, 3.0, 4.0])
    y = np.array([0, 1, 1, 0])
    t, _ = best_threshold(x, y)
    assert np.isclose(t, 1.5)


def test_gain_never_exceeds_parent_entropy():
    rng = np.random.default_rng(5)
    x = rng.normal(size=50)
    y = rng.integers(0, 4, size=50)
    _, gain = best_threshold(x, y)
    assert 0.0 <= gain <= _h(y) + 1e-9


def test_returns_python_floats():
    t, gain = best_threshold(np.array([0.0, 1.0]), np.array([0, 1]))
    assert isinstance(t, float) and isinstance(gain, float)
