"""
pytest data/app_data/01-classical-ml/03-decision-trees/03-best-split-minimal-tree/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-classical-ml/03-decision-trees/{Path(__file__).resolve().parent.name}")
find_best_split = _module.find_best_split
build_tree = _module.build_tree
predict_tree = _module.predict_tree


def test_best_split_finds_the_obvious_threshold():
    # A single feature that perfectly separates two classes at x=2.5 --
    # the only sensible best split.
    input = np.array([[1.0], [2.0], [3.0], [4.0]])
    labels = np.array([0, 0, 1, 1])
    feature, threshold, gain = find_best_split(input, labels)
    assert feature == 0
    assert 2.0 < threshold < 3.0
    assert gain > 0.0


def test_best_split_returns_none_for_a_pure_node():
    input = np.array([[1.0], [2.0], [3.0]])
    labels = np.array([1, 1, 1])
    assert find_best_split(input, labels) is None


def test_best_split_picks_the_informative_feature_over_the_useless_one():
    # feature 0 is random noise, feature 1 perfectly predicts the label
    # -- the search must not settle for the first feature just because
    # it's tried first.
    rng = np.random.default_rng(0)
    n = 40
    useless = rng.normal(size=n)
    useful = np.concatenate([np.zeros(20), np.ones(20)])
    labels = np.concatenate([np.zeros(20, dtype=int), np.ones(20, dtype=int)])
    input = np.column_stack([useless, useful])
    feature, _, _ = find_best_split(input, labels)
    assert feature == 1


def test_build_tree_on_pure_labels_is_a_single_leaf():
    input = np.array([[1.0], [2.0], [3.0]])
    labels = np.array([1, 1, 1])
    tree = build_tree(input, labels, max_depth=5)
    assert tree["leaf"] is True
    assert tree["prediction"] == 1


def test_build_tree_respects_max_depth_zero():
    # max_depth=0 must return a leaf immediately, no matter how mixed
    # the labels are -- the majority class of the whole node.
    input = np.array([[1.0], [2.0], [3.0], [4.0]])
    labels = np.array([0, 0, 1, 1])
    tree = build_tree(input, labels, max_depth=0)
    assert tree["leaf"] is True


def test_quadrant_pattern_needs_and_gets_depth_two():
    # Label is 1 only in the top-right quadrant (x>0 AND y>0), 0
    # everywhere else -- no single axis-aligned split separates this
    # perfectly, but two levels do: split x first (the x<=0 half is
    # already pure), then split y within the x>0 half. This exercises
    # the recursive part specifically, not just find_best_split alone.
    input = np.array(
        [[1.0, 1.0], [1.0, -1.0], [-1.0, 1.0], [-1.0, -1.0]] * 10
    )
    labels = np.array([1, 0, 0, 0] * 10)
    tree = build_tree(input, labels, max_depth=2)
    predictions = predict_tree(tree, input)
    assert np.array_equal(predictions, labels)


def test_true_xor_cannot_be_solved_by_greedy_single_step_lookahead():
    # A real, well-known limitation of greedy top-down tree induction,
    # not a bug: true XOR (exactly two diagonal quadrants share a
    # label) gives every possible single split zero information gain
    # at the root, greedy search never takes a first step, so
    # find_best_split correctly returns None even with samples left to
    # split and depth budget remaining.
    input = np.array(
        [[-1.0, -1.0], [-1.0, 1.0], [1.0, -1.0], [1.0, 1.0]] * 10
    )
    labels = np.array([0, 1, 1, 0] * 10)
    assert find_best_split(input, labels) is None
    tree = build_tree(input, labels, max_depth=5)
    assert tree["leaf"] is True


def test_predict_tree_walks_a_hand_built_tree_correctly():
    # A hand-assembled tree, independent of build_tree entirely, so
    # this isolates predict_tree's own traversal logic.
    tree = {
        "leaf": False,
        "feature": 0,
        "threshold": 5.0,
        "left": {"leaf": True, "prediction": 0},
        "right": {
            "leaf": False,
            "feature": 1,
            "threshold": 0.0,
            "left": {"leaf": True, "prediction": 1},
            "right": {"leaf": True, "prediction": 2},
        },
    }
    input = np.array([[1.0, 100.0], [10.0, -1.0], [10.0, 1.0]])
    predictions = predict_tree(tree, input)
    assert np.array_equal(predictions, [0, 1, 2])


def test_deeper_tree_never_has_lower_training_accuracy():
    # A real property of greedy tree growth: more depth can only add
    # splits that were chosen because they had positive gain, so
    # training accuracy is monotonically non-decreasing in max_depth.
    rng = np.random.default_rng(2)
    input = rng.normal(size=(60, 3))
    labels = (input[:, 0] + input[:, 1] ** 2 > 0.5).astype(int)
    accuracies = []
    for depth in (1, 2, 4, 8):
        tree = build_tree(input, labels, max_depth=depth)
        predictions = predict_tree(tree, input)
        accuracies.append(np.mean(predictions == labels))
    assert all(a <= b + 1e-9 for a, b in zip(accuracies, accuracies[1:]))


def test_matches_real_sklearn_decision_tree_accuracy_on_a_baked_dataset():
    # Ground truth from the actual library, not our own derivation.
    #
    # Generated once, offline, with:
    #   from sklearn.tree import DecisionTreeClassifier
    #   from sklearn.datasets import make_classification
    #   X, y = make_classification(n_samples=60, n_features=3,
    #       n_informative=2, n_redundant=0, n_classes=2, random_state=5)
    #   clf = DecisionTreeClassifier(criterion='gini', max_depth=3, random_state=0)
    #   clf.fit(X, y)
    #   clf.score(X, y)  # == 0.9833333333333333
    #
    # This test needs no scikit-learn installed to run -- the dataset
    # and the reference accuracy are baked in below. Our greedy,
    # single-feature-threshold, Gini-maximizing search is the same
    # algorithm scikit-learn's CART implementation runs, so it should
    # reach the same training accuracy on the same data.
    input = np.array(
        [
            [-1.2796, 1.0865, -0.7953], [-1.1184, -1.6397, 1.6353], [1.2222, -0.6325, 1.145],
            [0.7472, -1.2323, -1.1298], [0.4985, -0.8798, 0.4735], [1.1472, 2.351, 3.5566],
            [-0.4142, 0.4163, -0.2137], [-1.2641, 1.2233, 1.3727], [-0.0938, 0.1985, -0.4282],
            [-0.8139, 0.7306, 0.53], [1.2123, 1.4056, 0.1899], [-0.0347, 0.6512, -1.7168],
            [-0.2242, 0.622, 0.2752], [0.4651, 0.9174, -1.0085], [0.4763, 0.4313, -0.1046],
            [2.0736, 0.6164, -0.1674], [0.9563, 1.284, 1.5616], [-0.6464, 1.4451, -0.157],
            [0.2105, 0.1962, -1.2839], [0.2498, 0.7792, 0.6078], [-1.5997, -2.3332, -1.6424],
            [-0.8894, -1.1029, -1.0535], [1.4439, -0.9436, 0.7479], [1.4631, -1.7952, -1.3529],
            [-0.1431, 1.3523, 1.6763], [0.4137, -0.6024, 0.9955], [0.3056, 1.2188, -0.755],
            [-0.301, -1.2445, 1.8367], [-1.065, 0.4864, -1.3146], [-0.6347, -1.1148, -0.9843],
            [0.0365, 0.7095, -1.8294], [-0.5103, -1.0311, 0.8481], [0.443, -0.8593, 1.1407],
            [0.8772, -1.8505, -1.3975], [0.4677, -1.255, 0.4667], [-2.3867, -0.8676, 1.1732],
            [0.7098, -2.036, -1.4918], [-1.0385, 0.6238, 0.2964], [2.2333, 0.4913, -1.3486],
            [1.64, -0.0404, -0.6235], [-0.7061, -0.2926, 1.1961], [0.9275, -1.1072, -1.0776],
            [0.8359, 0.0027, -0.9618], [-0.0557, -1.3292, -1.1736], [0.1013, -1.3977, 0.8646],
            [1.4652, -2.5187, -1.7045], [0.2874, 1.5931, 2.0955], [0.5486, 0.668, -0.8503],
            [0.3904, 0.4465, -1.1889], [-1.301, 1.1111, -1.3503], [1.4022, 1.0376, -0.9811],
            [1.7384, -0.5828, -0.7658], [0.5218, 0.8561, -1.1108], [-0.6385, 0.9477, 0.8609],
            [-0.5732, 1.1594, 1.3206], [0.3465, 0.8571, -1.3887], [-0.5671, -1.4373, 1.1992],
            [0.5173, -1.0179, 0.6736], [-0.0594, -1.5433, 0.8151], [-0.1717, 1.4651, 1.8242],
        ]
    )
    labels = np.array(
        [1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1,
         0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0,
         0, 1]
    )
    tree = build_tree(input, labels, max_depth=3)
    predictions = predict_tree(tree, input)
    accuracy = np.mean(predictions == labels)
    assert np.isclose(accuracy, 0.9833333333333333, atol=1e-9)
