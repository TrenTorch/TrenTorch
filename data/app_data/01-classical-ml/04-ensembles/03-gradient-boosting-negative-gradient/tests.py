"""
pytest data/app_data/01-classical-ml/04-ensembles/03-gradient-boosting-negative-gradient/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-classical-ml/04-ensembles/{Path(__file__).resolve().parent.name}")
negative_gradient = _module.negative_gradient
fit_tree_to_negative_gradient = _module.fit_tree_to_negative_gradient
predict_regression_tree = load_solution(
    "01-classical-ml/03-decision-trees/05-regression-trees"
).predict_regression_tree


def test_negative_gradient_is_target_minus_prediction():
    targets = np.array([5.0, 3.0, -1.0])
    predictions = np.array([4.0, 3.0, 1.0])
    result = negative_gradient(targets, predictions)
    assert np.allclose(result, [1.0, 0.0, -2.0])


def test_negative_gradient_is_zero_at_a_perfect_prediction():
    targets = np.array([1.0, 2.0, 3.0])
    assert np.allclose(negative_gradient(targets, targets.copy()), 0.0)


def test_negative_gradient_sign_is_not_flipped():
    # Directly targets the "computed prediction - target instead of
    # target - prediction" mutant -- an under-prediction (target above
    # prediction) must give a POSITIVE residual, not negative.
    targets = np.array([10.0])
    predictions = np.array([2.0])
    assert negative_gradient(targets, predictions)[0] > 0


def test_fit_tree_recovers_targets_when_starting_predictions_are_zero():
    # With predictions all 0, the residual IS the target, so the fitted
    # tree should reproduce the same step-function targets exactly,
    # same as fitting a regression tree directly to them.
    input = np.array([[1.0], [2.0], [3.0], [4.0]] * 4)
    targets = np.array([0.0, 0.0, 10.0, 10.0] * 4)
    predictions = np.zeros_like(targets)
    tree = fit_tree_to_negative_gradient(input, targets, predictions, max_depth=3)
    recovered = predict_regression_tree(tree, input)
    assert np.allclose(recovered, targets)


def test_fit_tree_targets_the_remaining_error_not_the_original_target():
    # Predictions already capture most of the pattern -- the fitted
    # tree's job is the small remaining residual, not the original
    # (much larger) targets.
    rng = np.random.default_rng(0)
    input = rng.normal(size=(50, 2))
    targets = 3 * input[:, 0] + rng.normal(scale=0.2, size=50)
    predictions = 3 * input[:, 0]  # already very close to targets
    tree = fit_tree_to_negative_gradient(input, targets, predictions, max_depth=3)
    residual_predictions = predict_regression_tree(tree, input)
    # the fitted residuals should be small, tracking the leftover
    # noise, not anywhere near the scale of the original targets
    assert np.std(residual_predictions) < np.std(targets)


def test_adding_the_fitted_tree_reduces_squared_error():
    # The actual point of the exercise, checked end to end: current
    # predictions + this tree's output must fit the targets better
    # than current predictions alone.
    rng = np.random.default_rng(1)
    input = rng.normal(size=(60, 2))
    targets = input[:, 0] ** 2 + rng.normal(scale=0.1, size=60)
    predictions = np.full(60, np.mean(targets))  # a naive constant starting point

    tree = fit_tree_to_negative_gradient(input, targets, predictions, max_depth=3)
    updated_predictions = predictions + predict_regression_tree(tree, input)

    error_before = np.mean((targets - predictions) ** 2)
    error_after = np.mean((targets - updated_predictions) ** 2)
    assert error_after < error_before
