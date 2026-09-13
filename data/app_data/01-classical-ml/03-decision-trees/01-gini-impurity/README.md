---
name: decision-trees-gini-impurity
title: Gini Impurity for a split
tags: [classical-ml, decision-trees, splitting-criteria]
difficulty: Beginner
---

## Statement

### The problem, from first principles

A tree needs a way to tell whether the labels arriving at a node agree. Pure nodes need no more splitting; mixed nodes may benefit from it. Gini impurity summarizes that label mixture without assuming class labels are consecutive integers.

### From theory to code

Implement `gini_impurity(labels)` by counting each distinct label, converting counts to proportions, and applying the impurity formula. Theory also defines the empty-node convention used by later split logic.

### Constraints

- `labels` is a one-dimensional array of arbitrary integer class labels.
- Return a Python `float` in `[0, 1)`.
- Return exactly `0.0` for an empty array and for a pure node.
- Count distinct labels with `np.unique(..., return_counts=True)`.
- Use vectorized NumPy reductions; do not loop through labels.

### Hints

Open one at a time. Each gives away a little more than the last.

<details><summary>Hint 1</summary>

Only class frequencies matter; label values such as `5` and `7` are no different from `0` and `1`.

</details>

<details><summary>Hint 2</summary>

Divide counts by `labels.size`, square every proportion, sum them, then subtract from one.

</details>

## Theory

### The simple version

Gini impurity is the chance that two independently selected labels from a node disagree. A single-class bucket has no chance of disagreement; a balanced bucket has more.

### The formula

```text
if labels.size == 0: return 0.0
probabilities = unique-label counts / labels.size
gini = 1.0 - sum(probabilities ** 2)
```

### How PyTorch actually implements this

Context only, untested by your submission: this is a tree-splitting statistic rather than a standard `torch.nn` operation; tensor `unique` and reduction operations can express the same calculation.

## Explanation

The explicit `labels.size == 0` branch prevents division by zero and fixes empty-child impurity at `0.0`. `np.unique(labels, return_counts=True)` correctly handles arbitrary class identifiers. The resulting `counts / labels.size` are probabilities, and `float(1.0 - np.sum(probabilities**2))` returns the probability-of-disagreement form as a Python scalar.
