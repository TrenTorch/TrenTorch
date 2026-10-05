"""
pytest tests.py
"""

import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
leading_principal_minors = _module.leading_principal_minors
is_positive_definite_sylvester = _module.is_positive_definite_sylvester
classify_definiteness = _module.classify_definiteness
critical_point_type = _module.critical_point_type


def _random_pd(n, seed):
    b = np.random.default_rng(seed).normal(size=(n, n))
    return b @ b.T + np.eye(n)


# ---- 1-4: leading principal minors ----


def test_1_minors_hand_computed():
    a = np.array([[2.0, 1.0, 0.0], [1.0, 3.0, 1.0], [0.0, 1.0, 4.0]])
    # 2, 2*3 - 1 = 5, then det(a) = 2*(12-1) - 1*(4-0) = 18
    np.testing.assert_allclose(leading_principal_minors(a), [2.0, 5.0, 18.0])


def test_2_last_minor_is_the_determinant():
    a = np.random.default_rng(0).normal(size=(4, 4))
    assert np.isclose(leading_principal_minors(a)[-1], np.linalg.det(a))


def test_3_minors_of_a_one_by_one_matrix():
    np.testing.assert_allclose(leading_principal_minors(np.array([[7.0]])), [7.0])


def test_4_minors_have_length_n():
    assert leading_principal_minors(np.eye(5)).shape == (5,)


# ---- 5-8: Sylvester's criterion ----


def test_5_random_positive_definite_matrices_pass():
    for seed in range(6):
        assert is_positive_definite_sylvester(_random_pd(4, seed))


def test_6_a_zero_minor_fails_the_strict_test():
    assert not is_positive_definite_sylvester(np.array([[1.0, 1.0], [1.0, 1.0]]))


def test_7_indefinite_and_negative_definite_fail():
    assert not is_positive_definite_sylvester(np.array([[1.0, 2.0], [2.0, 1.0]]))
    assert not is_positive_definite_sylvester(-np.eye(3))


def test_8_non_symmetric_and_non_square_fail():
    assert not is_positive_definite_sylvester(np.array([[2.0, 5.0], [0.0, 2.0]]))
    assert not is_positive_definite_sylvester(np.ones((2, 3)))


# ---- 9-15: the five classes ----


def test_9_positive_definite():
    assert classify_definiteness(np.diag([1.0, 2.0, 3.0])) == "positive definite"


def test_10_positive_semidefinite():
    assert classify_definiteness(np.array([[1.0, 1.0], [1.0, 1.0]])) == "positive semidefinite"


def test_11_negative_definite():
    assert classify_definiteness(-_random_pd(3, 1)) == "negative definite"


def test_12_negative_semidefinite():
    assert classify_definiteness(np.array([[-1.0, 1.0], [1.0, -1.0]])) == "negative semidefinite"
    assert classify_definiteness(np.diag([0.0, -1.0])) == "negative semidefinite"


def test_13_indefinite():
    assert classify_definiteness(np.array([[0.0, 1.0], [1.0, 0.0]])) == "indefinite"
    assert classify_definiteness(np.diag([2.0, -1.0, 0.0])) == "indefinite"


def test_14_zero_matrix():
    assert classify_definiteness(np.zeros((3, 3))) == "zero"


def test_15_tolerance_treats_tiny_eigenvalues_as_zero():
    a = np.diag([2.0, 1e-12])
    assert classify_definiteness(a) == "positive semidefinite"
    assert classify_definiteness(a, tol=0.0) == "positive definite"
    assert classify_definiteness(np.diag([2.0, -1e-3])) == "indefinite"


def test_16_classification_agrees_with_sylvester_for_positive_definiteness():
    for seed in range(10):
        b = np.random.default_rng(seed).normal(size=(3, 3))
        a = (b + b.T) / 2
        assert (classify_definiteness(a) == "positive definite") == is_positive_definite_sylvester(a)


def test_17_negation_swaps_positive_and_negative_classes():
    pairs = {
        "positive definite": "negative definite",
        "positive semidefinite": "negative semidefinite",
        "indefinite": "indefinite",
    }
    for a in (np.diag([1.0, 2.0]), np.array([[1.0, 1.0], [1.0, 1.0]]), np.array([[0.0, 1.0], [1.0, 0.0]])):
        assert classify_definiteness(-a) == pairs[classify_definiteness(a)]


def test_18_invalid_input_raises_value_error():
    with pytest.raises(ValueError):
        classify_definiteness(np.array([[1.0, 2.0], [0.0, 1.0]]))
    with pytest.raises(ValueError):
        classify_definiteness(np.ones((2, 3)))


# ---- 19-22: critical points ----


def test_19_bowl_is_a_local_minimum():
    # f = x^2 + y^2 has Hessian 2 I
    assert critical_point_type(2 * np.eye(2)) == "local minimum"


def test_20_hilltop_is_a_local_maximum():
    assert critical_point_type(np.diag([-2.0, -4.0])) == "local maximum"


def test_21_pass_is_a_saddle_point():
    # f = x^2 - y^2 has Hessian diag(2, -2)
    assert critical_point_type(np.diag([2.0, -2.0])) == "saddle point"


def test_22_flat_directions_are_inconclusive():
    # f = x^4 + y^2: Hessian at the origin is diag(0, 2)
    assert critical_point_type(np.diag([0.0, 2.0])) == "inconclusive"
    assert critical_point_type(np.zeros((2, 2))) == "inconclusive"
    assert critical_point_type(np.diag([0.0, -2.0])) == "inconclusive"


def test_23_non_symmetric_hessian_raises_value_error():
    with pytest.raises(ValueError):
        critical_point_type(np.array([[1.0, 2.0], [0.0, 1.0]]))
