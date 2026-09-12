---
name: decision-trees-information-gain
title: Information Gain for a split
tags: [classical-ml, decision-trees, splitting-criteria]
difficulty: Beginner
---

## Statement

Implement:

```python
def information_gain(
    parent_labels: np.ndarray,
    left_labels: np.ndarray,
    right_labels: np.ndarray,
) -> float:
    """
    parent_labels: labels of every sample in the node before splitting.
    left_labels, right_labels: parent_labels partitioned by the
    candidate split, every sample in exactly one of the two.

    Returns:
        how much the split reduces Gini impurity, a float.
    """
```

- `left_labels` and `right_labels` together contain every sample in `parent_labels`, in some order, no sample is dropped or duplicated.
- Reuse `01-gini-impurity`'s `gini_impurity` rather than reimplementing it.

## Theory

`01-gini-impurity` measures how mixed a single node is. A decision tree needs more than that, it needs to compare _candidate splits_ against each other and pick the best one. Information gain is that comparison: how much purer are the two children, combined, than the parent was.

```text
Gain = Gini(parent) - [ (n_left/n) * Gini(left) + (n_right/n) * Gini(right) ]
```

The children's impurities are weighted by how many samples land in each, not averaged plainly, a split that sends 99% of samples into a perfectly pure left child and 1% into a messy right child is still a very good split, weighting by size is what lets the formula reflect that instead of penalizing it as much as an even 50/50 split would.

Gain is never negative: splitting a node can only maintain or reduce total impurity, never increase it, this is a real mathematical property of Gini impurity (it's concave), not just an empirical tendency. A tree-building algorithm searches many candidate splits and picks whichever one maximizes this number.

## Explanation

`gini_impurity(parent_labels)` computes the "before" impurity once. The weighted "after" impurity is `(left_labels.size / n) * gini_impurity(left_labels) + (right_labels.size / n) * gini_impurity(right_labels)`, using each child's own sample count relative to the parent's total, not `0.5` each.

The function is only ever `parent_impurity - weighted_child_impurity`, in that order, gain is how much impurity was _removed_, so a good split (children purer than the parent) gives a positive number.
