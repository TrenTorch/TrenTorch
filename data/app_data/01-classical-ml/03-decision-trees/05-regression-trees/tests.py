"""
pytest data/app_data/01-classical-ml/03-decision-trees/05-regression-trees/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-classical-ml/03-decision-trees/{Path(__file__).resolve().parent.name}")
variance = _module.variance
variance_reduction = _module.variance_reduction
find_best_regression_split = _module.find_best_regression_split
build_regression_tree = _module.build_regression_tree
predict_regression_tree = _module.predict_regression_tree


def test_variance_of_constant_targets_is_zero():
    assert variance(np.array([5.0, 5.0, 5.0])) == 0.0


def test_variance_matches_hand_computation():
    # mean=2, squared diffs 1,0,1 -> mean 2/3.
    assert np.isclose(variance(np.array([1.0, 2.0, 3.0])), 2.0 / 3.0)


def test_variance_of_empty_is_zero_by_convention():
    assert variance(np.array([], dtype=float)) == 0.0


def test_variance_reduction_perfect_split_matches_hand_computation():
    # parent=[0,0,10,10], var=25. Both children constant -> var 0 each.
    # reduction = 25 - 0 = 25.
    parent = np.array([0.0, 0.0, 10.0, 10.0])
    left = np.array([0.0, 0.0])
    right = np.array([10.0, 10.0])
    assert np.isclose(variance_reduction(parent, left, right), 25.0)


def test_variance_reduction_weights_by_child_size_not_evenly():
    # Directly targets the "used 0.5/0.5 instead of size-proportional
    # weights" mutant, same shape as information_gain's analogous test.
    parent = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 10.0, 0.0, 10.0])
    left = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 10.0])  # size 6
    right = np.array([0.0, 10.0])  # size 2
    var_parent = variance(parent)
    var_left, var_right = variance(left), variance(right)
    expected = var_parent - ((6 / 8) * var_left + (2 / 8) * var_right)
    assert np.isclose(variance_reduction(parent, left, right), expected)
    # the incorrect 0.5/0.5 weighting would give a different number
    wrong = var_parent - (0.5 * var_left + 0.5 * var_right)
    assert not np.isclose(expected, wrong)


def test_find_best_regression_split_finds_the_obvious_step():
    input = np.array([[1.0], [2.0], [3.0], [4.0]])
    targets = np.array([0.0, 0.0, 10.0, 10.0])
    feature, threshold, reduction = find_best_regression_split(input, targets)
    assert feature == 0
    assert 2.0 < threshold < 3.0
    assert np.isclose(reduction, 25.0)


def test_find_best_regression_split_returns_none_for_constant_targets():
    input = np.array([[1.0], [2.0], [3.0]])
    targets = np.array([7.0, 7.0, 7.0])
    assert find_best_regression_split(input, targets) is None


def test_build_and_predict_recover_a_step_function():
    input = np.array([[1.0], [2.0], [3.0], [4.0]] * 5)
    targets = np.array([0.0, 0.0, 10.0, 10.0] * 5)
    tree = build_regression_tree(input, targets, max_depth=3)
    predictions = predict_regression_tree(tree, input)
    assert np.allclose(predictions, targets)


def test_predictions_are_floats_not_truncated_to_int():
    input = np.array([[1.0], [2.0]])
    targets = np.array([1.5, 2.5])
    tree = build_regression_tree(input, targets, max_depth=1)
    predictions = predict_regression_tree(tree, input)
    assert predictions.dtype == np.float64


def test_leaf_prediction_is_the_mean_not_a_class_vote():
    # A regression leaf must average, not pick a "majority" value --
    # targets here have no repeated value at all, so a classification-
    # style vote has nothing sensible to fall back to.
    input = np.array([[1.0], [1.0], [1.0]])
    targets = np.array([2.0, 4.0, 9.0])
    tree = build_regression_tree(input, targets, max_depth=0)
    assert tree["leaf"] is True
    assert np.isclose(tree["prediction"], 5.0)  # mean of 2, 4, 9


def test_matches_real_sklearn_decision_tree_regressor_on_a_baked_dataset():
    # Ground truth from the actual library, not our own derivation.
    #
    # Generated once, offline, with:
    #   rng = np.random.default_rng(9)
    #   X = rng.normal(size=(40, 2))
    #   y = 2*X[:,0] - 1.5*X[:,1]**2 + rng.normal(scale=0.3, size=40)
    #   reg = DecisionTreeRegressor(criterion='squared_error', max_depth=3, random_state=0)
    #   reg.fit(X, y)
    #   np.mean((reg.predict(X) - y)**2)  # == 0.5745549012418859
    #
    # This test needs no scikit-learn installed to run -- the dataset
    # and reference MSE are baked in below.
    input = np.array(
        [
            [-0.8028, 0.2428], [-1.6563, 0.6561], [1.1435, -0.4526], [0.4305, 0.2509],
            [-0.3944, -0.8624], [-2.0326, 1.4104], [-0.0476, 2.5223], [0.8262, 0.2778],
            [-0.6574, 1.3925], [-0.5063, 1.5699], [-0.3984, 0.186], [-1.5227, 2.3432],
            [-0.094, -0.3851], [0.8108, -0.8914], [0.7676, -1.1712], [0.5452, -1.0441],
            [-1.8371, -0.5938], [-1.4639, 0.5533], [0.0217, 0.5094], [0.0913, -0.3539],
            [0.0281, 1.0525], [-0.1831, -0.762], [-0.9699, -0.2217], [-0.7497, 1.8806],
            [-1.1786, -1.0816], [-0.3059, 0.65], [-0.2681, -0.9579], [-0.8069, -0.3508],
            [0.9734, -0.978], [-0.0913, -0.6131], [0.3246, 0.3971], [-1.4652, 2.3869],
            [0.1896, -0.5093], [-0.894, -0.2595], [0.0318, 0.5952], [0.0056, 0.4839],
            [-1.61, -0.7524], [-1.0066, 0.1646], [0.458, -1.4661], [-0.1679, 0.7255],
        ]
    )
    targets = np.array(
        [-1.4196, -4.293, 2.1485, 0.868, -2.0351, -6.4601, -9.9741, 1.4535, -4.0869, -4.6368,
         -0.9, -10.8684, 0.0231, 0.7037, -0.222, -0.5613, -4.5524, -2.7307, -0.6332, 0.6636,
         -1.6435, -1.1678, -2.0643, -6.5172, -4.2643, -0.6926, -1.7521, -1.746, 0.341, -0.6622,
         0.4117, -10.9062, 0.2709, -2.357, -0.009, -1.052, -3.6068, -2.6195, -2.3079, -0.8816]
    )
    tree = build_regression_tree(input, targets, max_depth=3)
    predictions = predict_regression_tree(tree, input)
    mse = np.mean((predictions - targets) ** 2)
    assert np.isclose(mse, 0.5745549012418859, atol=1e-6)
