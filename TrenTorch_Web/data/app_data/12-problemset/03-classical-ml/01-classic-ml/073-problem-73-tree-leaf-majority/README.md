---
name: problem-73-tree-leaf-majority
title: 'Tree Leaf Majority'
tags: [problemset, classical-ml-trees-ensembles, decision-trees]
difficulty: Beginner
kind: problemset
relatedModule: 'part-classical-ml|Classic ML'
topic: 'decision trees'
hint: 'np.unique with counts, then argmax of the counts'
tools: [NumPy]
---

## Statement

Return the majority class among the labels that reach a leaf of a decision tree. If several classes tie for the highest count, return the smallest label.

Implement `solve(y)`.

**Returns.** Return the winning label (a scalar taken from `y`).

### Examples

**Example 1**

Input:

```python
solve([0, 1, 1, 0, 1])
```

Output:

```text
1
```

**Example 2**

Input:

```python
solve([2, 2, 3, 3])
```

Output:

```text
2
```

## Theory

### The simple version

A decision-tree leaf predicts the most common class among the training samples that landed in it. It is the cheapest possible rule and, for a pure leaf, the only sensible one.

### The rule

$$\hat c=\arg\max_{c}\;\#\{i: y_i=c\}$$

## Explanation

`np.unique` returns the distinct labels in sorted order together with their counts, and `argmax` returns the first maximum, so ties are broken toward the smaller label. That makes the prediction deterministic.
