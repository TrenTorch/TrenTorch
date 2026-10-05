"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
s3vm_objective = _module.s3vm_objective

W = np.array([1.0, 0.0])
EMPTY = np.zeros((0, 2))


def _raises_value_error(function, *args, **kwargs):
    try:
        function(*args, **kwargs)
    except ValueError:
        return True
    return False


def test_hand_example_with_one_labeled_and_one_unlabeled():
    # Regularizer 0.5. Labeled f = 2, hinge 0. Unlabeled f = 0.5, hinge 0.5 * C_u = 1.0.
    J = s3vm_objective(W, 0.0, np.array([[2.0, 0.0]]), np.array([1]), np.array([[0.5, 0.0]]), 1.0, 2.0)
    assert np.isclose(J, 1.5)


def test_wrong_sign_labeled_point_pays_full_hinge():
    # f = 2, y = -1, hinge = 1 + 2 = 3, regularizer 0.5.
    J = s3vm_objective(W, 0.0, np.array([[2.0, 0.0]]), np.array([-1]), EMPTY, 1.0, 0.0)
    assert np.isclose(J, 3.5)


def test_unlabeled_point_beyond_margin_adds_nothing():
    J_with = s3vm_objective(W, 0.0, np.array([[2.0, 0.0]]), np.array([1]), np.array([[3.0, 0.0]]), 1.0, 5.0)
    J_without = s3vm_objective(W, 0.0, np.array([[2.0, 0.0]]), np.array([1]), EMPTY, 1.0, 5.0)
    assert np.isclose(J_with, J_without)


def test_unlabeled_point_on_either_side_is_penalized_equally():
    J_pos = s3vm_objective(W, 0.0, EMPTY.reshape(0, 2), np.array([]), np.array([[0.4, 0.0]]), 1.0, 1.0)
    J_neg = s3vm_objective(W, 0.0, EMPTY.reshape(0, 2), np.array([]), np.array([[-0.4, 0.0]]), 1.0, 1.0)
    assert np.isclose(J_pos, J_neg)
    assert np.isclose(J_pos, 0.5 + 0.6)


def test_zero_unlabeled_weight_reduces_to_svm_hinge():
    X_l = np.array([[0.5, 0.0], [-2.0, 0.0]])
    y_l = np.array([1, -1])
    J = s3vm_objective(W, 0.0, X_l, y_l, np.array([[0.1, 0.0]]), 1.0, 0.0)
    assert np.isclose(J, 0.5 + (1 - 0.5) + 0.0)


def test_bias_shifts_scores():
    X_l = np.array([[0.0, 0.0]])
    y_l = np.array([1])
    base = s3vm_objective(W, 0.0, X_l, y_l, EMPTY, 1.0, 0.0)
    shifted = s3vm_objective(W, 1.0, X_l, y_l, EMPTY, 1.0, 0.0)
    assert np.isclose(base, 0.5 + 1.0)
    assert np.isclose(shifted, 0.5)


def test_regularizer_grows_with_weight_norm():
    w_small = np.array([0.5, 0.0])
    w_big = np.array([2.0, 0.0])
    small = s3vm_objective(w_small, 0.0, EMPTY, np.array([]), EMPTY, 0.0, 0.0)
    big = s3vm_objective(w_big, 0.0, EMPTY, np.array([]), EMPTY, 0.0, 0.0)
    assert np.isclose(small, 0.125) and np.isclose(big, 2.0)


def test_empty_unlabeled_set_is_allowed():
    J = s3vm_objective(W, 0.0, np.array([[1.0, 0.0]]), np.array([1]), EMPTY, 1.0, 9.0)
    assert np.isclose(J, 0.5)


def test_scaling_c_scales_labeled_term_only():
    X_l = np.array([[0.0, 0.0]])
    y_l = np.array([1])
    one = s3vm_objective(W, 0.0, X_l, y_l, EMPTY, 1.0, 0.0)
    three = s3vm_objective(W, 0.0, X_l, y_l, EMPTY, 3.0, 0.0)
    assert np.isclose(three - one, 2.0)


def test_non_binary_label_raises():
    assert _raises_value_error(s3vm_objective, W, 0.0, np.array([[1.0, 0.0]]), np.array([0]), EMPTY, 1.0, 1.0)


def test_negative_weight_raises():
    assert _raises_value_error(s3vm_objective, W, 0.0, EMPTY, np.array([]), EMPTY, -1.0, 1.0)


def test_feature_dimension_mismatch_raises():
    assert _raises_value_error(s3vm_objective, W, 0.0, np.array([[1.0, 0.0, 0.0]]), np.array([1]), EMPTY, 1.0, 1.0)


def test_inputs_are_not_modified():
    X_l = np.array([[2.0, 0.0]])
    y_l = np.array([1])
    before = X_l.copy()
    s3vm_objective(W, 0.0, X_l, y_l, EMPTY, 1.0, 1.0)
    assert np.array_equal(X_l, before)
