"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

cosine_similarity = load_solution(__file__).cosine_similarity


def test_same_direction_is_one():
    assert np.isclose(cosine_similarity(np.array([1.0, 2.0]), np.array([2.0, 4.0])), 1.0)


def test_opposite_direction_is_minus_one():
    assert np.isclose(cosine_similarity(np.array([1.0, 2.0]), np.array([-1.0, -2.0])), -1.0)


def test_perpendicular_is_zero():
    assert np.isclose(cosine_similarity(np.array([1.0, 0.0]), np.array([0.0, 3.0])), 0.0)


def test_hand_computed_value():
    # (1*4 + 2*5 + 3*6) / (sqrt(14) * sqrt(77))
    assert np.isclose(cosine_similarity(np.array([1.0, 2.0, 3.0]), np.array([4.0, 5.0, 6.0])), 32 / np.sqrt(14 * 77))


def test_scale_invariant():
    rng = np.random.default_rng(0)
    a, b = rng.normal(size=5), rng.normal(size=5)
    assert np.isclose(cosine_similarity(a, b), cosine_similarity(7.0 * a, 0.1 * b))


def test_zero_vector_returns_zero():
    assert cosine_similarity(np.zeros(3), np.array([1.0, 2.0, 3.0])) == 0.0


def test_within_bounds_and_symmetric():
    rng = np.random.default_rng(1)
    for _ in range(20):
        a, b = rng.normal(size=6), rng.normal(size=6)
        value = cosine_similarity(a, b)
        assert -1.0 - 1e-12 <= value <= 1.0 + 1e-12
        assert np.isclose(value, cosine_similarity(b, a))


def test_returns_python_float():
    assert isinstance(cosine_similarity(np.array([1.0, 0.0]), np.array([1.0, 1.0])), float)
