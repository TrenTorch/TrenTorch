"""
pytest data/app_data/01-classical-ml/03-decision-trees/04-pruning/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-classical-ml/03-decision-trees/{Path(__file__).resolve().parent.name}")
build_tree_pre_pruned = _module.build_tree_pre_pruned
prune_tree = _module.prune_tree
predict_tree = load_solution(
    "01-classical-ml/03-decision-trees/03-best-split-minimal-tree"
).predict_tree


def _count_nodes(tree: dict) -> int:
    if tree["leaf"]:
        return 1
    return 1 + _count_nodes(tree["left"]) + _count_nodes(tree["right"])


def test_min_samples_leaf_blocks_a_split_that_would_isolate_one_sample():
    # 4 zeros then one lone 1 -- the obvious split isolates a single
    # sample on one side. With min_samples_leaf=2 that split must be
    # refused, this node stays a single leaf even though depth remains.
    input = np.array([[1.0], [2.0], [3.0], [4.0], [5.0]])
    labels = np.array([0, 0, 0, 0, 1])
    tree = build_tree_pre_pruned(input, labels, max_depth=5, min_samples_leaf=2)
    assert tree["leaf"] is True


def test_min_samples_leaf_one_allows_the_same_split():
    input = np.array([[1.0], [2.0], [3.0], [4.0], [5.0]])
    labels = np.array([0, 0, 0, 0, 1])
    tree = build_tree_pre_pruned(input, labels, max_depth=5, min_samples_leaf=1)
    assert tree["leaf"] is False


def test_every_node_carries_a_default_field():
    input = np.array([[1.0], [2.0], [3.0], [4.0]])
    labels = np.array([0, 0, 1, 1])
    tree = build_tree_pre_pruned(input, labels, max_depth=5)
    assert "default" in tree
    assert "default" in tree["left"]
    assert "default" in tree["right"]


def test_prune_tree_leaves_an_already_leaf_tree_unchanged():
    leaf = {"leaf": True, "prediction": 1, "default": 1}
    input_val = np.array([[1.0, 2.0], [3.0, 4.0]])
    labels_val = np.array([1, 0])
    pruned = prune_tree(leaf, input_val, labels_val)
    assert pruned == leaf


def test_reduced_error_pruning_collapses_a_spurious_branch():
    # A hand-built tree, independent of build_tree_pre_pruned: root
    # splits on feature 0 (genuinely predictive), the left branch then
    # splits again on feature 1 (spurious -- doesn't generalize).
    # Validation data shows feature 1 doesn't help in that branch, so
    # reduced-error pruning must collapse it to a single leaf, while
    # leaving the genuinely useful root split alone.
    tree = {
        "leaf": False,
        "feature": 0,
        "threshold": 0.0,
        "default": 0,
        "left": {
            "leaf": False,
            "feature": 1,
            "threshold": 0.0,
            "default": 0,
            "left": {"leaf": True, "prediction": 0, "default": 0},
            "right": {"leaf": True, "prediction": 1, "default": 0},
        },
        "right": {"leaf": True, "prediction": 1, "default": 0},
    }
    input_val = np.array([[-1.0, -1.0], [-1.0, 1.0], [-1.0, 1.0], [1.0, 0.0]])
    labels_val = np.array([0, 0, 0, 1])

    pruned = prune_tree(tree, input_val, labels_val)

    assert pruned["leaf"] is False  # root split is still worth keeping
    assert pruned["left"]["leaf"] is True  # spurious sub-split collapsed
    assert pruned["left"]["prediction"] == 0
    assert pruned["right"]["leaf"] is True  # already a leaf, untouched
    assert pruned["right"]["prediction"] == 1


def test_pruning_never_increases_validation_error():
    # The actual guarantee reduced-error pruning makes: the pruned
    # tree's validation error is never worse than the original's,
    # checked across a genuinely overfit tree on noisy data, not just
    # the one hand-picked case above.
    rng = np.random.default_rng(3)
    input_train = rng.normal(size=(60, 3))
    labels_train = (input_train[:, 0] > 0).astype(int)
    # flip a few training labels so a deep tree "explains" noise
    flip_idx = rng.choice(60, size=6, replace=False)
    labels_train[flip_idx] = 1 - labels_train[flip_idx]

    input_val = rng.normal(size=(40, 3))
    labels_val = (input_val[:, 0] > 0).astype(int)

    tree = build_tree_pre_pruned(input_train, labels_train, max_depth=8, min_samples_leaf=1)
    pruned = prune_tree(tree, input_val, labels_val)

    original_error = np.sum(predict_tree(tree, input_val) != labels_val)
    pruned_error = np.sum(predict_tree(pruned, input_val) != labels_val)
    assert pruned_error <= original_error
    assert _count_nodes(pruned) <= _count_nodes(tree)


def test_pruning_uses_validation_samples_routed_to_the_correct_side():
    # Directly targets a plausible bug: comparing against the *entire*
    # labels_val at every node instead of the subset actually routed to
    # that node. Root's own children get very different validation
    # subsets here (left: majority label 0, right: entirely label 1),
    # a "used the whole labels_val everywhere" bug would compute the
    # same (wrong) majority/error at both nodes.
    tree = {
        "leaf": False,
        "feature": 0,
        "threshold": 0.0,
        "default": 0,
        "left": {"leaf": True, "prediction": 0, "default": 0},
        "right": {
            "leaf": False,
            "feature": 1,
            "threshold": 0.0,
            "default": 0,
            "left": {"leaf": True, "prediction": 0, "default": 0},
            "right": {"leaf": True, "prediction": 1, "default": 0},
        },
    }
    # left side (feature0<=0): 5 samples, all label 0 -- pruning right's
    # subtree should not be influenced by these at all.
    # right side (feature0>0): the right subtree's own split on feature1
    # perfectly separates its 4 samples -- must NOT be pruned away.
    input_val = np.array(
        [
            [-1.0, 5.0], [-1.0, 5.0], [-1.0, 5.0], [-1.0, 5.0], [-1.0, 5.0],
            [1.0, -1.0], [1.0, -1.0], [1.0, 1.0], [1.0, 1.0],
        ]
    )
    labels_val = np.array([0, 0, 0, 0, 0, 0, 0, 1, 1])
    pruned = prune_tree(tree, input_val, labels_val)
    assert pruned["right"]["leaf"] is False
