---
name: problem-58-knn-regression
title: 'KNN Regression'
tags: [problemset, classical-ml, knn]
difficulty: Advanced
kind: problemset
relatedModule: 'part-classical-ml|Classification'
topic: 'knn'
hint: 'stable argsort of squared distances, mean of the k nearest targets'
tools: [NumPy]
---

## Statement

Predict a numeric target for a query point as the average target of its `k` nearest training rows (squared Euclidean distance). Distance ties are resolved in favour of the earlier training row.

Implement `solve(X,y,q,k)`.

**Returns.** Return the prediction as a Python float.

### Examples

**Example 1**

Input:

```python
solve([[0.0], [1.0], [2.0], [10.0]], [1.0, 2.0, 3.0, 100.0], [1.2], 2)
```

Output:

```text
2.5
```

**Example 2**

Input:

```python
solve([[0.0], [4.0]], [10.0, 20.0], [1.0], 2)
```

Output:

```text
15.0
```

## Theory

### The simple version

KNN regression is the same idea as KNN classification, except the neighbours' targets are _averaged_ instead of voted on. With $k=1$ it copies the nearest target; with $k=n$ it always predicts the global mean.

### The formula

$$\hat y(q)=\frac1k\sum_{i\in N_k(q)}y_i$$

### Why it matters

- KNN regression predicts a number by averaging nearby targets, a flexible model with no assumed shape.
- The choice of $k$ trades noise (small $k$) against blur (large $k$).

### How it works

1. Squared distances from the query to every training row.
2. Take the $k$ nearest.
3. Average their targets.

### Worked example

The query $1.2$ is closest to $1$ (distance $0.2$) and then $2$ (distance $0.8$), so the two nearest targets are $2$ and $3$, and their mean is 2.5.

## Explanation

Small $k$ follows the data closely but is noisy; large $k$ is smoother but can blur real structure. In the first example the two nearest targets, $2$ and $3$, are averaged to $2.5$, while the far-away outlier $100$ is ignored. With $k=n$ it would be dragged into the average.
