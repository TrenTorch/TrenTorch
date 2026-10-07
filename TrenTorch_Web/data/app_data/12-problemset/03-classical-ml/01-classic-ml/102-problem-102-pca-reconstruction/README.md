---
name: problem-102-pca-reconstruction
title: 'PCA Reconstruction'
tags: [problemset, unsupervised-ml, pca]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-classical-ml|Classic ML'
topic: 'pca'
hint: 'Z @ components[:, :k].T + mean'
tools: [NumPy]
---

## Statement

Reconstruct data from its PCA coordinates: map the `k` retained coordinates back to the original feature space and add the mean back, $\hat X=Z\,V[:, :k]^\top+\mu$.

Implement `solve(Z, components, k, mean)`.

**Returns.** Return an $n\times d$ NumPy array.

### Examples

**Example 1**

Input:

```python
solve([[1.0], [3.0]], [[1.0, 0.0], [0.0, 1.0]], 1, [10.0, 20.0])
```

Output:

```text
[[11.0, 20.0], [13.0, 20.0]]
```

**Example 2**

Input:

```python
solve([[2.0, -1.0]], [[0.0, 1.0], [1.0, 0.0]], 2, [0.0, 0.0])
```

Output:

```text
[[-1.0, 2.0]]
```

## Theory

### The simple version

Compression is only useful if you can get something back. Multiplying the kept coordinates by the transposed component matrix returns them to the original axes, and adding the mean undoes the earlier centring. If $k<d$ the reconstruction is an approximation, because the dropped directions are lost.

### The formula

$$\hat X=Z\,V_k^\top+\mu$$

## Explanation

With $k=d$ and orthonormal components the reconstruction is exact. In the first example only the first coordinate is kept, so the second feature is reconstructed as just its mean, $20$.
