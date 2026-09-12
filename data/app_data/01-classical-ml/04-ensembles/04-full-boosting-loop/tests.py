"""
pytest data/app_data/01-classical-ml/04-ensembles/04-full-boosting-loop/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-classical-ml/04-ensembles/{Path(__file__).resolve().parent.name}")
train_gradient_boosting = _module.train_gradient_boosting
predict_gradient_boosting = _module.predict_gradient_boosting


def test_initial_prediction_is_the_target_mean():
    input = np.array([[1.0], [2.0], [3.0]])
    targets = np.array([2.0, 4.0, 6.0])
    initial_prediction, _ = train_gradient_boosting(
        input, targets, n_trees=0, max_depth=2, learning_rate=0.1
    )
    assert np.isclose(initial_prediction, 4.0)


def test_zero_trees_predicts_the_constant_everywhere():
    input = np.array([[1.0], [2.0], [3.0]])
    targets = np.array([2.0, 4.0, 6.0])
    initial_prediction, trees = train_gradient_boosting(
        input, targets, n_trees=0, max_depth=2, learning_rate=0.1
    )
    assert trees == []
    predictions = predict_gradient_boosting(initial_prediction, trees, 0.1, input)
    assert np.allclose(predictions, 4.0)


def test_zero_learning_rate_leaves_predictions_at_the_constant():
    # Directly targets a mutant that forgets to apply learning_rate at
    # all (or applies it only during training, not prediction): with
    # learning_rate=0, every tree's contribution must vanish entirely.
    rng = np.random.default_rng(0)
    input = rng.normal(size=(30, 2))
    targets = rng.normal(size=30)
    initial_prediction, trees = train_gradient_boosting(
        input, targets, n_trees=5, max_depth=2, learning_rate=0.0
    )
    predictions = predict_gradient_boosting(initial_prediction, trees, 0.0, input)
    assert np.allclose(predictions, initial_prediction)


def test_more_trees_reduces_training_error():
    rng = np.random.default_rng(1)
    input = rng.normal(size=(80, 2))
    targets = input[:, 0] ** 2 - input[:, 1] + rng.normal(scale=0.1, size=80)

    errors = []
    for n_trees in (1, 5, 20):
        initial_prediction, trees = train_gradient_boosting(
            input, targets, n_trees=n_trees, max_depth=3, learning_rate=0.3
        )
        predictions = predict_gradient_boosting(initial_prediction, trees, 0.3, input)
        errors.append(np.mean((predictions - targets) ** 2))
    assert errors[0] > errors[1] > errors[2]


def test_predict_replays_training_accumulation_exactly_on_training_data():
    rng = np.random.default_rng(2)
    input = rng.normal(size=(40, 2))
    targets = rng.normal(size=40)
    initial_prediction, trees = train_gradient_boosting(
        input, targets, n_trees=8, max_depth=2, learning_rate=0.2
    )
    # Manually replay the exact same accumulation from scratch and
    # confirm predict_gradient_boosting matches it, not just "close".
    predict_regression_tree = load_solution(
        "01-classical-ml/03-decision-trees/05-regression-trees"
    ).predict_regression_tree
    manual = np.full(40, initial_prediction)
    for tree in trees:
        manual = manual + 0.2 * predict_regression_tree(tree, input)
    predictions = predict_gradient_boosting(initial_prediction, trees, 0.2, input)
    assert np.allclose(predictions, manual)


def test_matches_real_sklearn_gradient_boosting_regressor_on_a_baked_dataset():
    # Ground truth from the actual library, not our own derivation.
    #
    # Generated once, offline, with:
    #   rng = np.random.default_rng(11)
    #   X = rng.normal(size=(50, 2))
    #   y = 2*X[:,0] - X[:,1]**2 + rng.normal(scale=0.2, size=50)
    #   gbr = GradientBoostingRegressor(n_estimators=10, max_depth=2,
    #       learning_rate=0.3, random_state=0)
    #   gbr.fit(X, y)
    #   np.mean((gbr.predict(X) - y)**2)  # == 0.13713298649625846
    #
    # This test needs no scikit-learn installed to run.
    input = np.array(
        [
            [0.0342, 1.3597], [1.2247, -0.5103], [-0.298, -0.5274], [0.5697, -0.0561],
            [0.7469, -1.8473], [1.5665, -0.0964], [0.6804, -0.1366], [-0.3791, 0.4631],
            [0.8245, -0.2025], [-0.1528, 0.6857], [-0.8703, -1.5144], [0.395, -0.6706],
            [-1.9203, -0.8141], [-0.4676, -1.1932], [-1.4925, 0.0366], [0.8972, -0.2331],
            [-0.7436, 0.385], [0.7172, -0.3], [0.5447, 1.0429], [-0.207, -0.8135],
            [0.3477, 0.2475], [1.0988, -1.2846], [-0.6616, -0.8382], [-1.734, 0.1264],
            [0.5278, -0.7388], [1.3856, 0.8219], [0.6274, 0.4017], [0.9557, -1.332],
            [0.6139, 0.6028], [-1.7677, 0.347], [-0.2504, 0.7815], [-0.4391, -0.0182],
            [0.3429, -0.8763], [0.5986, -0.105], [0.4925, -0.5218], [1.0862, 0.6052],
            [-0.178, 0.632], [1.2598, 1.7912], [-1.5736, 0.8831], [0.4651, -0.0939],
            [-1.0067, 1.2572], [-1.2617, 0.5669], [1.3019, -1.5997], [-0.3025, -1.3092],
            [0.2441, 1.5144], [2.0236, -1.7781], [-0.5749, 0.7035], [1.5794, 0.4212],
            [-0.7462, 0.2971], [-0.0166, -0.2037],
        ]
    )
    targets = np.array(
        [-1.9274, 2.2665, -0.8125, 1.1177, -1.9632, 2.8668, 1.2449, -0.7314, 1.5699, -1.0637,
         -3.7672, 0.4464, -4.0817, -2.3464, -3.0785, 1.4506, -1.3706, 1.8584, -0.1624, -1.2051,
         0.7533, 0.3814, -2.0799, -3.554, 0.5482, 2.3147, 1.0978, 0.321, 0.7805, -3.5903,
         -1.5393, -1.1684, 0.0771, 1.0681, 0.8286, 1.9146, -0.491, -0.5264, -3.7237, 0.899,
         -3.7335, -2.9912, -0.0528, -2.5451, -1.9147, 0.8669, -1.5946, 2.9135, -1.9653, -0.0892]
    )
    initial_prediction, trees = train_gradient_boosting(
        input, targets, n_trees=10, max_depth=2, learning_rate=0.3
    )
    predictions = predict_gradient_boosting(initial_prediction, trees, 0.3, input)
    mse = np.mean((predictions - targets) ** 2)
    assert np.isclose(mse, 0.13713298649625846, atol=1e-6)
