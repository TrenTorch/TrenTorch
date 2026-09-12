---
name: decision-trees-feature-importance
title: Feature importance from a fitted tree
tags: [classical-ml, decision-trees, interpretability]
difficulty: Intermediate
---

## Statement

Implement:

```python
def feature_importances(
    tree: dict, input: np.ndarray, labels: np.ndarray, n_features: int
) -> np.ndarray:
    """
    tree: a tree from build_tree (03-best-split-minimal-tree), fitted
    on (input, labels).

    Returns:
        shape (n_features,), summing to 1 (or all zeros for a
        single-leaf tree).
    """
```

- Reuse `02-information-gain`'s `information_gain`, don't reimplement it.
- Re-derive each node's data subset by walking the tree with `input`/`labels`, the same way `predict_tree` walks it, rather than assuming the tree stores its own data.

## Theory

A fitted tree already embodies which features mattered, wherever a feature was chosen for a split, it's because that split reduced impurity more than any alternative available at that node. Feature importance turns that fact into one number per feature: sum up how much impurity every split on that feature removed, across the whole tree, weighted by how many samples that split actually affected.

```text
for every split node in the tree:
    weight = (samples reaching this node) / (total samples)
    importance[feature used at this node] += weight * information_gain(at this node)

normalize importances to sum to 1
```

The weighting by sample count matters for the same reason it mattered in `02-information-gain` itself: a split near the root affects every sample, a split three levels deep in a small branch only affects the handful of samples that reached it. A feature used once at the root with high gain can easily matter more than a feature used in several small, deep splits, and the weighting is what lets the numbers reflect that instead of just counting "how many times was this feature used."

Real `scikit-learn`'s `DecisionTreeClassifier.feature_importances_` is exactly this computation (Gini-based "mean decrease in impurity"), computed once at fit time from statistics the tree already stored internally while building.

## Explanation

`feature_importances` re-walks the tree from the root, carrying `input`/`labels` alongside it and partitioning them at every split node using that node's own `feature`/`threshold`, the identical routing `predict_tree` uses, just applied to the training data instead of a query point, and recursing into both children instead of picking one.

At each split node, `information_gain(node_labels, left_labels, right_labels)` recomputes the exact gain that split achieved (the tree itself doesn't store this number, so it's recomputed from the data), and `node_labels.size / total_samples` is the weight, this node's share of the full dataset. `importances[feature] += weight * gain` accumulates credit into the right slot even when the same feature is split on more than once in different parts of the tree.

The final `importances / importances.sum()` (guarded against a single-leaf tree, whose sum is `0`) rescales the raw weighted-gain totals into the conventional "importances sum to 1" form, so importances are comparable across trees of different sizes and depths, not just within one tree.
