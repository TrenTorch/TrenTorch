---
name: problem-57-knn-classification
title: 'KNN Classification'
tags: [problemset, classical-ml, knn]
difficulty: Advanced
kind: problemset
relatedModule: 'part-classical-ml|Classification'
topic: 'knn'
hint: 'stable argsort of squared distances, take k, then the most common label (smallest on ties)'
tools: [NumPy]
---

## Statement

Predict the class of a query point by a majority vote among its `k` nearest training rows (squared Euclidean distance). Distance ties are resolved in favour of the earlier training row, and a tied vote goes to the class that sorts first.

Implement `solve(X, labels, q, k)`.

**Returns.** Return the winning class label, taken from `labels`.

### Examples

**Example 1**

Input:

```python
solve([[0.0], [1.0], [10.0], [11.0]], [0, 0, 1, 1], [0.5], 3)
```

Output:

```text
0
```

**Example 2**

Input:

```python
solve([[0.0], [2.0]], ['a', 'b'], [1.0], 2)
```

Output:

```text
'a'
```

## Theory

### The simple version

k-nearest-neighbours has no training step. To classify a new point, find the $k$ closest stored examples and let them vote. It assumes that nearby points tend to share a class.

### The recipe

1. Compute the distance from the query to every training row.
2. Take the indices of the $k$ smallest distances (stable sort, so ties keep the earlier row).
3. Count the labels among them; the most frequent wins.

## Explanation

Squared distances give the same ordering as true distances and skip the square root. `np.unique` returns the classes in sorted order, and `argmax` returns the first maximum, which is exactly the "smallest class wins a tie" rule. In the second example both neighbours are equally close and vote once each, so the smaller label `'a'` wins.
