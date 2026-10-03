"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
dual_objective = _module.dual_objective
is_dual_feasible = _module.is_dual_feasible


def _raises_value_error(function, *args, **kwargs):
    try:
        function(*args, **kwargs)
    except ValueError:
        return True
    return False


def test_zero_alpha_gives_zero_objective():
    assert dual_objective(np.zeros(3), np.array([1.0, -1.0, 1.0]), np.eye(3)) == 0.0


def test_identity_kernel_with_opposite_labels():
    # sum(alpha) = 2 and ay = [1, -1] has squared norm 2, so W = 2 - 0.5 * 2 = 1.
    assert np.isclose(dual_objective([1.0, 1.0], [1.0, -1.0], np.eye(2)), 1.0)


def test_all_ones_kernel_with_balanced_labels_has_no_quadratic_term():
    # (sum alpha_i y_i)^2 = 0 when K is all ones, so W = sum(alpha) = 2.
    assert np.isclose(dual_objective([1.0, 1.0], [1.0, -1.0], np.ones((2, 2))), 2.0)


def test_single_point_objective_is_t_minus_half_t_squared():
    for t in [0.5, 1.0, 2.0]:
        assert np.isclose(dual_objective([t], [1.0], [[1.0]]), t - t * t / 2)


def test_flipping_all_labels_leaves_objective_unchanged():
    alpha = np.array([0.3, 0.7, 0.2])
    y = np.array([1.0, -1.0, 1.0])
    K = np.array([[2.0, 0.5, 0.1], [0.5, 1.0, 0.3], [0.1, 0.3, 1.5]])
    assert np.isclose(dual_objective(alpha, y, K), dual_objective(alpha, -y, K))


def test_kernel_shape_mismatch_raises():
    assert _raises_value_error(dual_objective, [1.0, 1.0], [1.0, -1.0], np.eye(3))


def test_label_length_mismatch_raises():
    assert _raises_value_error(dual_objective, [1.0, 1.0], [1.0], np.eye(2))


def test_feasible_point_passes():
    assert is_dual_feasible([0.5, 0.5], [1.0, -1.0], C=1.0)


def test_alpha_above_the_box_is_infeasible():
    assert not is_dual_feasible([1.5, 1.5], [1.0, -1.0], C=1.0)


def test_negative_alpha_is_infeasible():
    assert not is_dual_feasible([-0.1, 0.1], [1.0, -1.0], C=1.0)


def test_unbalanced_weights_are_infeasible():
    assert not is_dual_feasible([1.0, 0.0], [1.0, -1.0], C=10.0)


def test_zero_box_allows_only_zero_alpha():
    assert is_dual_feasible([0.0, 0.0], [1.0, -1.0], C=0.0)
    assert not is_dual_feasible([0.1, 0.1], [1.0, -1.0], C=0.0)


def test_rounding_inside_tolerance_is_accepted():
    assert is_dual_feasible([0.5 + 1e-12, 0.5], [1.0, -1.0], C=1.0)


def test_negative_C_raises():
    assert _raises_value_error(is_dual_feasible, [0.5, 0.5], [1.0, -1.0], -1.0)
