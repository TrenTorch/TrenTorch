"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
steering_vector = _module.steering_vector
apply_steering = _module.apply_steering


def test_1_hand_computed_difference_of_means():
    pos = np.array([[2.0, 0.0], [4.0, 2.0]])
    neg = np.array([[1.0, 1.0], [1.0, 1.0]])
    assert np.allclose(steering_vector(pos, neg, normalize=False), [2.0, 0.0])


def test_2_normalized_vector_has_unit_length():
    rng = np.random.RandomState(0)
    v = steering_vector(rng.randn(10, 6) + 1, rng.randn(8, 6))
    assert np.isclose(np.linalg.norm(v), 1.0)


def test_3_identical_sets_give_zero_vector_without_nan():
    a = np.ones((3, 4))
    v = steering_vector(a, a.copy())
    assert np.all(v == 0.0)


def test_4_apply_to_selected_positions_only():
    resid = np.zeros((4, 2))
    out = apply_steering(resid, np.array([1.0, -1.0]), 2.0, positions=[1, 3])
    assert np.allclose(out, [[0, 0], [2, -2], [0, 0], [2, -2]])


def test_5_apply_to_all_positions_by_default():
    out = apply_steering(np.ones((3, 2)), np.array([0.5, 0.5]), 2.0)
    assert np.allclose(out, 2.0)


def test_6_steering_moves_the_projection_by_alpha():
    rng = np.random.RandomState(1)
    resid = rng.randn(5, 8)
    v = steering_vector(rng.randn(6, 8) + 2, rng.randn(6, 8))
    out = apply_steering(resid, v, 3.0)
    assert np.allclose(out @ v - resid @ v, 3.0)


def test_7_input_not_modified():
    resid = np.random.RandomState(2).randn(4, 3)
    snap = resid.copy()
    apply_steering(resid, np.ones(3), 1.0, positions=[0, 2])
    assert np.array_equal(resid, snap)
