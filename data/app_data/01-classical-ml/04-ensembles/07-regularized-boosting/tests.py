"""
pytest data/app_data/01-classical-ml/04-ensembles/07-regularized-boosting/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-classical-ml/04-ensembles/{Path(__file__).resolve().parent.name}")
xgboost_leaf_value = _module.xgboost_leaf_value
xgboost_split_gain = _module.xgboost_split_gain
find_best_regularized_split = _module.find_best_regularized_split
train_regularized_boosting = _module.train_regularized_boosting
predict_regularized_boosting = _module.predict_regularized_boosting

plain_gb = load_solution("01-classical-ml/04-ensembles/04-full-boosting-loop")


def test_leaf_value_matches_hand_computation_at_lam_zero():
    gradients = np.array([1.0, -1.0, 2.0])
    hessians = np.array([1.0, 1.0, 1.0])
    assert np.isclose(xgboost_leaf_value(gradients, hessians, lam=0.0), -2.0 / 3.0)


def test_leaf_value_shrinks_toward_zero_as_lambda_grows():
    gradients = np.array([1.0, -1.0, 2.0])
    hessians = np.array([1.0, 1.0, 1.0])
    unregularized = xgboost_leaf_value(gradients, hessians, lam=0.0)
    regularized = xgboost_leaf_value(gradients, hessians, lam=10.0)
    assert abs(regularized) < abs(unregularized)


def test_split_gain_matches_hand_computation():
    gradients = np.array([-2.0, -2.0, 2.0, 2.0])
    hessians = np.array([1.0, 1.0, 1.0, 1.0])
    left_mask = np.array([True, True, False, False])
    # G=0, H=4 -> parent term = 0/4 = 0
    # left: G=-4, H=2 -> 16/2 = 8; right: G=4, H=2 -> 16/2 = 8
    # gain = 0.5 * (8 + 8 - 0) = 8.0
    assert np.isclose(xgboost_split_gain(gradients, hessians, left_mask, lam=0.0), 8.0)


def test_split_gain_decreases_with_larger_lambda():
    gradients = np.array([-2.0, -2.0, 2.0, 2.0])
    hessians = np.array([1.0, 1.0, 1.0, 1.0])
    left_mask = np.array([True, True, False, False])
    gain_no_reg = xgboost_split_gain(gradients, hessians, left_mask, lam=0.0)
    gain_regularized = xgboost_split_gain(gradients, hessians, left_mask, lam=5.0)
    assert gain_regularized < gain_no_reg


def test_find_best_regularized_split_finds_the_obvious_split():
    input = np.array([[1.0], [2.0], [3.0], [4.0]])
    gradients = np.array([-5.0, -5.0, 5.0, 5.0])
    hessians = np.ones(4)
    feature, threshold, gain = find_best_regularized_split(input, gradients, hessians, lam=0.0)
    assert feature == 0
    assert 2.0 < threshold < 3.0
    assert gain > 0.0


def test_lambda_zero_matches_plain_gradient_boosting_closely():
    # A real internal consistency check: with lam=0 and squared-error
    # loss (constant hessians), the regularized gain formula reduces to
    # the same comparison 05-regression-trees's variance reduction
    # makes, so the two boosters should reach nearly the same fit.
    rng = np.random.default_rng(11)
    input = rng.normal(size=(50, 2))
    targets = 2 * input[:, 0] - input[:, 1] ** 2 + rng.normal(scale=0.2, size=50)

    plain_init, plain_trees = plain_gb.train_gradient_boosting(
        input, targets, n_trees=10, max_depth=2, learning_rate=0.3
    )
    plain_predictions = plain_gb.predict_gradient_boosting(plain_init, plain_trees, 0.3, input)
    plain_mse = np.mean((plain_predictions - targets) ** 2)

    reg_init, reg_trees = train_regularized_boosting(
        input, targets, n_trees=10, max_depth=2, learning_rate=0.3, lam=0.0
    )
    reg_predictions = predict_regularized_boosting(reg_init, reg_trees, 0.3, input)
    reg_mse = np.mean((reg_predictions - targets) ** 2)

    assert np.isclose(plain_mse, reg_mse, atol=1e-3)


def test_heavier_regularization_increases_training_error():
    # The actual point of the exercise: a large lam should visibly pull
    # leaves toward 0 and hurt the training fit, compared to lam=0 on
    # the same data.
    rng = np.random.default_rng(11)
    input = rng.normal(size=(50, 2))
    targets = 2 * input[:, 0] - input[:, 1] ** 2 + rng.normal(scale=0.2, size=50)

    init_low, trees_low = train_regularized_boosting(
        input, targets, n_trees=10, max_depth=2, learning_rate=0.3, lam=0.0
    )
    init_high, trees_high = train_regularized_boosting(
        input, targets, n_trees=10, max_depth=2, learning_rate=0.3, lam=50.0
    )
    mse_low = np.mean((predict_regularized_boosting(init_low, trees_low, 0.3, input) - targets) ** 2)
    mse_high = np.mean(
        (predict_regularized_boosting(init_high, trees_high, 0.3, input) - targets) ** 2
    )
    assert mse_high > mse_low


def test_leaf_value_denominator_includes_lambda_not_just_hessians():
    # Directly targets a mutant that computes -G/H and adds lam
    # somewhere else (or not at all): with H=3 and lam=3, the correct
    # denominator is 6, exactly half of the unregularized H alone.
    gradients = np.array([3.0, 3.0, 3.0])
    hessians = np.array([1.0, 1.0, 1.0])
    assert np.isclose(xgboost_leaf_value(gradients, hessians, lam=3.0), -1.5)
