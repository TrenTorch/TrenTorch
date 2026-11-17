"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

softmax_probabilities = load_solution(__file__).softmax_probabilities


def test_hand_computed_probabilities():
    p = softmax_probabilities(np.array([0.0, np.log(3.0)]), 1.0)
    assert np.allclose(p, [0.25, 0.75])


def test_sums_to_one():
    rng = np.random.default_rng(0)
    for tau in (0.1, 1.0, 10.0):
        assert np.isclose(softmax_probabilities(rng.normal(size=6), tau).sum(), 1.0)


def test_high_temperature_approaches_uniform():
    p = softmax_probabilities(np.array([1.0, 5.0, 9.0]), 1e6)
    assert np.allclose(p, 1 / 3, atol=1e-4)


def test_low_temperature_approaches_greedy():
    p = softmax_probabilities(np.array([1.0, 5.0, 9.0]), 0.01)
    assert p[2] > 0.999


def test_shift_invariant():
    q = np.array([1.0, 2.0, 3.0])
    assert np.allclose(softmax_probabilities(q, 1.0), softmax_probabilities(q + 100.0, 1.0))


def test_no_overflow_for_large_values():
    p = softmax_probabilities(np.array([1000.0, 1001.0]), 1.0)
    assert np.all(np.isfinite(p)) and np.isclose(p.sum(), 1.0)


def test_better_arms_get_higher_probability():
    p = softmax_probabilities(np.array([0.1, 0.5, 0.9]), 0.5)
    assert p[0] < p[1] < p[2]
