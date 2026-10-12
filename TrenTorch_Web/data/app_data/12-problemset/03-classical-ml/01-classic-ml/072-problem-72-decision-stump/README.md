---
name: problem-72-decision-stump
title: 'Decision Stump'
tags: [problemset, classical-ml-trees-ensembles, decision-trees]
difficulty: Advanced
kind: problemset
relatedModule: 'part-classical-ml|Classic ML'
topic: 'decision trees'
hint: 'best Gini threshold, then the majority class on each side'
tools: [NumPy]
---

## Statement

Train a depth-1 decision tree (a stump) on one numeric feature. Choose the split `x <= t` / `x > t` with the smallest weighted Gini impurity (first minimum, so the smallest threshold wins ties), then predict the majority class on each side; a tied majority goes to the smaller class label.

Implement `solve(x, y)`.

**Returns.** Return a tuple `(threshold, left_class, right_class)`. If `x` has fewer than two distinct values there is nothing to split and `ValueError` is raised.

### Examples

**Example 1**

Input:

```python
solve([1.0, 2.0, 3.0, 4.0], [0, 0, 1, 1])
```

Output:

```text
(2.0, 0, 1)
```

**Example 2**

Input:

```python
solve([1.0, 2.0, 3.0, 4.0, 5.0], [1, 1, 1, 0, 0])
```

Output:

```text
(3.0, 1, 0)
```

**Example 3**

Input:

```python
solve([3.0, 3.0], [0, 1])
```

Output: Raises `ValueError`.

## Theory

### The simple version

A decision stump is the smallest possible classifier: one threshold on one feature and a class for each side. It is a weak learner on its own, but boosting methods such as AdaBoost combine many stumps into a strong model.

### The recipe

1. Pick the threshold with the lowest weighted Gini impurity.
2. Predict the most frequent class among the samples on each side.

### Why it matters

- A stump is the weakest useful classifier and the building block of boosting.
- It shows a tree's decision in its simplest form.

### How it works

1. Find the best threshold (as in best binary split).
2. Predict the majority class on each side.

### Worked example

The best threshold for $x=(1,2,3,4)$, $y=(0,0,1,1)$ is $2$. The left side holds only class $0$ and the right only class $1$, so the stump is (2.0, 0, 1).

## Explanation

The split search is the same as in the best-binary-split problem. Each side then votes by majority, and `np.unique` followed by `argmax` resolves ties toward the smaller label. A feature with a single distinct value cannot be split, so the function raises instead of returning a meaningless stump.
