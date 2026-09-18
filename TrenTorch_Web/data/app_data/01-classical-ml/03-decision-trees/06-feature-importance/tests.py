"""
pytest data/app_data/01-classical-ml/03-decision-trees/06-feature-importance/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

feature_importances = load_solution(
    f"01-classical-ml/03-decision-trees/{Path(__file__).resolve().parent.name}"
).feature_importances
build_tree = load_solution(
    "01-classical-ml/03-decision-trees/03-best-split-minimal-tree"
).build_tree


def test_single_leaf_tree_gives_all_zero_importances():
    tree = {"leaf": True, "prediction": 1}
    input = np.array([[1.0, 2.0], [3.0, 4.0]])
    labels = np.array([1, 1])
    result = feature_importances(tree, input, labels, n_features=2)
    assert np.allclose(result, [0.0, 0.0])


def test_tree_split_only_on_one_feature_gives_it_all_the_importance():
    input = np.array([[1.0, 100.0], [2.0, 100.0], [3.0, 100.0], [4.0, 100.0]])
    labels = np.array([0, 0, 1, 1])
    tree = build_tree(input, labels, max_depth=3)
    result = feature_importances(tree, input, labels, n_features=2)
    assert np.isclose(result[0], 1.0)
    assert np.isclose(result[1], 0.0)


def test_importances_sum_to_one_for_a_real_multi_split_tree():
    rng = np.random.default_rng(4)
    input = rng.normal(size=(80, 3))
    labels = ((input[:, 0] > 0).astype(int) + (input[:, 1] > 0.5).astype(int)) % 2
    tree = build_tree(input, labels, max_depth=4)
    result = feature_importances(tree, input, labels, n_features=3)
    assert np.isclose(result.sum(), 1.0)
    assert np.all(result >= 0.0)


def test_root_level_split_weighs_more_than_a_deep_small_split():
    # Directly targets the "forgot the (node_samples/total) weighting"
    # mutant: two hand-built trees where an unweighted sum would rate
    # the deep, tiny-node split as equally important as the root split
    # that touches every sample, but weighting by sample count must
    # not.
    input = np.array([[1.0, 1.0], [2.0, 1.0], [3.0, 5.0], [4.0, 5.0], [5.0, -5.0], [6.0, 5.0]])
    labels = np.array([0, 0, 1, 1, 1, 1])
    # Root splits on feature 0 at 2.5 (perfect, touches all 6 samples).
    # The right child then also splits on feature 1 to isolate the one
    # sample with value -5, a small, low-impact split by comparison.
    tree = build_tree(input, labels, max_depth=3)
    result = feature_importances(tree, input, labels, n_features=2)
    assert result[0] > result[1]


def test_matches_real_sklearn_feature_importances_on_a_baked_dataset():
    # Ground truth from the actual library, not our own derivation.
    #
    # Generated once, offline, with the same (X, y) as
    # 03-best-split-minimal-tree's baked oracle test:
    #   clf = DecisionTreeClassifier(criterion='gini', max_depth=3, random_state=0)
    #   clf.fit(X, y)
    #   clf.feature_importances_  # == [0.05314573, 0.87708683, 0.06976744]
    #
    # This test needs no scikit-learn installed to run.
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
    result = feature_importances(tree, input, labels, n_features=3)
    expected = np.array([0.05314573, 0.87708683, 0.06976744])
    assert np.allclose(result, expected, atol=1e-6)
