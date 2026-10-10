---
name: kmeans-assignment-company-211
title: 'kmeans-assignment — Meta case'
tags: [problemset, unsupervised-ml, k-means-clustering, meta]
difficulty: Beginner
kind: problemset
relatedModule: 'part-classical-ml|Classification'
topic: 'Classification'
caseCompany: 'Meta'
hint: 'argmin over centroids of squared distances'
tools: [NumPy]
---

## Statement

Meta-inspired content-clustering pipeline has a set of candidate centroids and needs to assign each embedding to its closest cluster. You need to perform the assignment step correctly so the clustering loop can continue.

Assign every embedding (row of `X`) to the closest centroid (row of `C`) using squared Euclidean distance. On a tie the lower centroid index wins.

Implement `solve(X,C)`.

**Returns.** Return an integer NumPy array with one centroid index per embedding.

Assign every embedding (row of `X`) to the closest centroid (row of `C`) using squared Euclidean distance. On a tie the lower centroid index wins.

Implement `solve(X,C)`.

**Returns.** Return an integer NumPy array with one centroid index per embedding.

### Examples

**Example 1**

Input:

```python
solve([[0, 0], [10, 0]], [[0, 1], [9, 0]])
```

Output:

```text
[0, 1]
```

**Example 2**

Input:

```python
solve([[1.0, 1.0]], [[0.0, 0.0], [2.0, 2.0]])
```

Output:

```text
[0]
```

## Theory

### The simple version

K-means alternates two steps. The _assignment_ step, implemented here, sends each point to its nearest centre; the _update_ step then moves each centre to the mean of its points.

### The rule

$$c_i=\arg\min_k\|x_i-\mu_k\|_2^2$$

### Why it matters

- The assignment step is half of every k-means iteration; the update step is the other half.
- Squared distances pick the same nearest centroid as true distances without a square root.

### How it works

1. Build the matrix of squared distances between every point and every centroid.
2. Take the column index of the smallest value in each row.

### Worked example

The point $(0,0)$ is $1$ from centroid $(0,1)$ and $81$ from $(9,0)$, so it goes to centroid $0$. The point $(10,0)$ is $101$ from the first and $1$ from the second, so it goes to centroid $1$: [0, 1].

## Explanation

Broadcasting builds all point-to-centroid squared distances at once. In the second example the point is exactly halfway between the two centroids, so the lower index $0$ wins.
