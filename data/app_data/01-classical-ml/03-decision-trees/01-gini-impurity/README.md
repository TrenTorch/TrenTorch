---
name: decision-trees-gini-impurity
title: Gini Impurity for a split
tags: [classical-ml, decision-trees, splitting-criteria]
difficulty: Beginner
---

## Statement

Implement:

```python
def gini_impurity(labels: np.ndarray) -> float:
    """
    labels: 1-D array of class labels (any integers, not necessarily
    0..k-1 or contiguous), one per sample in a single tree node.

    Returns:
        the Gini impurity of this set of labels, a float in [0, 1).
    """
```

- Works for any number of classes, not just binary.
- Labels don't need to be `0..k-1`, use whatever distinct values are actually present.
- An empty `labels` array has no impurity by convention, return `0.0`.
- A node where every label is identical is perfectly pure, `0.0`.

## Theory

A decision tree grows by repeatedly splitting a node's samples into two children, trying to make each child as "pure" as possible, ideally every sample in a child belongs to the same class. Gini impurity is one way to measure how far a node is from that ideal.

For a node with class proportions `p_1, ..., p_k` (each `p_c` is the fraction of this node's samples belonging to class `c`):

```text
Gini = 1 - sum(p_c^2 for c in classes)
```

Two useful readings of the same formula:

- `sum(p_c^2)` is the probability that two samples drawn independently (with replacement) from this node happen to land in the _same_ class. `1 -` that is the probability they land in _different_ classes, so Gini impurity is literally "how likely are two random samples from this node to disagree."
- A perfectly pure node (`p_c = 1` for one class, `0` for the rest) gives `Gini = 1 - 1 = 0`, the minimum. A node split evenly across `k` classes gives `Gini = 1 - k*(1/k)^2 = 1 - 1/k`, the maximum for that many classes, most "mixed up" a node can be.

`scikit-learn`'s `DecisionTreeClassifier(criterion='gini')` computes exactly this formula internally (in compiled Cython, not exposed as a standalone public function) at every candidate split, to decide which split reduces impurity the most, that comparison is `02-information-gain`, the next question in this track.

## Explanation

`np.unique(labels, return_counts=True)` gets the count of each distinct class actually present, without assuming labels are `0..k-1` or that every possible class shows up in this particular node.

`probabilities = counts / labels.size` turns raw counts into the `p_c` fractions Theory's formula uses. `1.0 - np.sum(probabilities ** 2)` is that formula directly, no loop needed since `np.sum` reduces over the whole `probabilities` array in one call.

The `labels.size == 0` check exists only to avoid dividing by zero, an empty node has no samples to be impure about, so `0.0` is the only sensible convention, not a computed value.
