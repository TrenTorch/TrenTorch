---
name: pairwise-distance-matrix-company-225
title: 'pairwise-distance-matrix — Pinterest case'
tags: [problemset, unsupervised-ml, k-means-clustering, pinterest]
difficulty: Beginner
kind: problemset
relatedModule: 'part-mathematics|Probability & Statistics'
topic: 'Probability & Statistics'
caseCompany: 'Pinterest'
hint: '((X[:,None,:] - X[None,:,:])**2).sum(axis=2)'
tools: [NumPy]
---

## Statement

Pinterest-inspired visual retrieval prototype compares a batch of item embeddings against every other item in the batch. You need to compute the pairwise squared-distance matrix efficiently and with the expected shape.

Compute the matrix of squared Euclidean distances between all pairs of rows of `X`: entry $(i,j)$ is $\|x_i-x_j\|^2$.

Implement `solve(X)`.

**Returns.** Return a symmetric $n\times n$ float NumPy matrix with zeros on the diagonal.

### Examples

**Example 1**

Input:

```python
solve([[0, 0], [3, 4]])
```

Output:

```text
[[0.0, 25.0], [25.0, 0.0]]
```

**Example 2**

Input:

```python
solve([[1.0], [2.0], [4.0]])
```

Output:

```text
[[0.0, 1.0, 9.0], [1.0, 0.0, 4.0], [9.0, 4.0, 0.0]]
```

## Theory

### The simple version

Retrieval compares every item with every other. Squared distances are enough for ranking neighbours (they order items the same way as true distances) and avoid the square root.

### The formula

$$D_{ij}=\sum_k(x_{ik}-x_{jk})^2$$

## Explanation

Broadcasting subtracts every row from every other row in one expression. The points $(0,0)$ and $(3,4)$ differ by $3$ and $4$, so their squared distance is $9+16=25$. For large $n$ the $O(n^2d)$ memory of this version can be reduced with the identity $\|a-b\|^2=\|a\|^2+\|b\|^2-2a\!\cdot\!b$.
