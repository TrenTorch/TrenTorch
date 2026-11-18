---
name: problem-101-101-pca-projection
title: 'PCA Projection'
tags: [problemset, pca]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-classical-ml|Classic ML'
topic: 'pca'
hint: 'X @ components[:, :k]'
---

## Statement

Project centred row data `X` onto the first `k` principal components. `components` is a matrix whose columns are the component directions, so the retained coordinates are $Z=X\,V[:, :k]$.

Implement `solve(X, components, k)`.

**Returns.** Return an $n\times k$ NumPy array.

### Examples

**Example 1**

Input:

```python
solve([[1, 2], [3, 4]], [[1, 0], [0, 1]], 1)
```

Output:

```text
[[1], [3]]
```

**Example 2**

Input:

```python
solve([[-1, 2]], [[0, 1], [1, 0]], 2)
```

Output:

```text
[[2, -1]]
```

## Theory

### The simple version

PCA is a rotation of the coordinate axes. Projecting the data onto the first $k$ new axes keeps the $k$ directions of greatest variation and throws the rest away, compressing the data to $k$ numbers per sample.

### The formula

$$Z=\tilde X\,V_k,\qquad V_k=V[:, :k]$$

### Why it matters

- Projection compresses data to $k$ numbers per sample while keeping the directions of greatest variance.
- It is a single matrix product.

### How it works

1. Take the first $k$ columns of the component matrix.
2. Multiply the (centred) data by them.

### Worked example

With the identity as component matrix and $k=1$ only the first axis is kept, so the data $(1,2)$ and $(3,4)$ project to $1$ and $3$: [[1], [3]].

## Explanation

The columns of $V$ are assumed to be orthonormal and sorted from the largest explained variance down, so the first $k$ columns are the top components. The second example swaps the two coordinates, so $(-1,2)\mapsto(2,-1)$.
