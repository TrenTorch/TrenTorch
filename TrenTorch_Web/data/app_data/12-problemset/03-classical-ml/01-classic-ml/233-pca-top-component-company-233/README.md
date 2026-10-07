---
name: pca-top-component-company-233
title: 'pca-top-component — Meesho case'
tags: [problemset, unsupervised-ml, pca, meesho]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-classical-ml|Classic ML'
topic: 'Classic ML'
caseCompany: 'Meesho'
hint: 'eigh of the covariance; take the last eigenvector; normalise and fix the sign'
tools: [NumPy]
---

## Statement

Meesho-inspired catalog analytics pipeline wants a one-dimensional summary of correlated product features. You need to compute the leading PCA direction so the team can project each product onto the dominant variance direction.

Return the first principal component of `X`: centre the data, form the population covariance matrix, and take the eigenvector of the largest eigenvalue. Scale it to unit length and flip its sign if necessary so that its entry of largest magnitude is positive (the first such entry on a tie).

Implement `solve(X)`.

**Returns.** Return a unit-norm float NumPy vector with one entry per feature.

### Examples

**Example 1**

Input:

```python
solve([[1, 1], [2, 2], [3, 3]])
```

Output:

```text
[0.707107, 0.707107]
```

**Example 2**

Input:

```python
solve([[1.0, 0.0], [-1.0, 0.0], [2.0, 0.1], [-2.0, -0.1]])
```

Output:

```text
[0.9992, 0.039984]
```

## Theory

### The simple version

PCA finds the single direction along which the data is most spread out. Projecting onto it gives the best one-dimensional summary. That direction is the eigenvector of the covariance matrix with the largest eigenvalue; the eigenvalue itself is the variance along it.

### The recipe

$$\Sigma=\tfrac1n\tilde X^\top\tilde X,\qquad \Sigma v=\lambda_{\max}v,\quad\|v\|=1$$

## Explanation

An eigenvector is only defined up to sign ($v$ and $-v$ are equally valid), so a sign rule is needed to make the answer deterministic. For points on the diagonal (first example) the direction is $(1,1)/\sqrt2\approx(0.707,0.707)$. `np.linalg.eigh` is used because the covariance matrix is symmetric.
