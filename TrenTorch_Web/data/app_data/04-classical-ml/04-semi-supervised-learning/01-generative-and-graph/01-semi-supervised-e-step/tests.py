"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
responsibilities = _module.responsibilities
semi_supervised_e_step = _module.semi_supervised_e_step

MEANS = np.array([[0.0], [2.0]])
COVS = np.array([[[1.0]], [[1.0]]])
PRIORS = np.array([0.5, 0.5])


def _raises_value_error(function, *args, **kwargs):
    try:
        function(*args, **kwargs)
    except ValueError:
        return True
    return False


def test_equal_priors_midpoint_gives_even_split():
    R = responsibilities(np.array([[1.0]]), MEANS, COVS, PRIORS)
    assert np.allclose(R, [[0.5, 0.5]])


def test_hand_computed_responsibility_matches_sigmoid_of_log_ratio():
    # log N(0|0,1) - log N(0|2,1) = 2, so r_0 = sigmoid(2).
    R = responsibilities(np.array([[0.0]]), MEANS, COVS, PRIORS)
    assert np.isclose(R[0, 0], 1 / (1 + np.exp(-2.0)))


def test_rows_sum_to_one():
    rng = np.random.default_rng(0)
    X = rng.normal(size=(20, 1)) * 3
    R = responsibilities(X, MEANS, COVS, PRIORS)
    assert np.allclose(R.sum(axis=1), 1.0)


def test_prior_shifts_responsibility_toward_likely_component():
    R = responsibilities(np.array([[1.0]]), MEANS, COVS, np.array([0.9, 0.1]))
    assert R[0, 0] > 0.5


def test_far_away_point_stays_finite():
    R = responsibilities(np.array([[1000.0]]), MEANS, COVS, PRIORS)
    assert np.all(np.isfinite(R))
    assert np.isclose(R.sum(), 1.0)


def test_multivariate_matches_isotropic_hand_value():
    means = np.array([[0.0, 0.0], [2.0, 0.0]])
    covs = np.stack([np.eye(2), np.eye(2)])
    R = responsibilities(np.array([[0.0, 0.0]]), means, covs, PRIORS)
    # Squared distance to the second mean is 4, so the log ratio is 4 / 2 = 2.
    assert np.isclose(R[0, 0], 1 / (1 + np.exp(-2.0)))


def test_semi_supervised_clamps_labeled_rows_to_one_hot():
    X = np.array([[0.0], [1.0], [2.0]])
    y = np.array([1, -1, 0])
    R = semi_supervised_e_step(X, y, MEANS, COVS, PRIORS)
    assert np.array_equal(R[0], [0.0, 1.0])
    assert np.array_equal(R[2], [1.0, 0.0])


def test_unlabeled_rows_keep_model_responsibilities():
    X = np.array([[0.0], [1.0]])
    y = np.array([-1, 1])
    R = semi_supervised_e_step(X, y, MEANS, COVS, PRIORS)
    assert np.allclose(R[0], responsibilities(X, MEANS, COVS, PRIORS)[0])


def test_all_unlabeled_equals_plain_responsibilities():
    X = np.array([[0.3], [1.7]])
    y = np.array([-1, -1])
    assert np.allclose(
        semi_supervised_e_step(X, y, MEANS, COVS, PRIORS),
        responsibilities(X, MEANS, COVS, PRIORS),
    )


def test_label_out_of_range_raises():
    assert _raises_value_error(semi_supervised_e_step, np.array([[0.0]]), np.array([2]), MEANS, COVS, PRIORS)


def test_priors_not_summing_to_one_raise():
    assert _raises_value_error(responsibilities, np.array([[0.0]]), MEANS, COVS, np.array([0.3, 0.3]))


def test_non_positive_definite_covariance_raises():
    bad = np.array([[[1.0]], [[-1.0]]])
    assert _raises_value_error(responsibilities, np.array([[0.0]]), MEANS, bad, PRIORS)


def test_shape_mismatch_raises():
    assert _raises_value_error(responsibilities, np.array([[0.0, 1.0]]), MEANS, COVS, PRIORS)


def test_inputs_are_not_modified():
    X = np.array([[0.0], [1.0]])
    y = np.array([0, -1])
    X0, y0 = X.copy(), y.copy()
    semi_supervised_e_step(X, y, MEANS, COVS, PRIORS)
    assert np.array_equal(X, X0) and np.array_equal(y, y0)
