---
name: problem-92-k-means-inertia
title: K-Means Inertia
tags: [unsupervised-ml, case-study, medium, clustering-evaluation., company-case]
difficulty: Intermediate
---

## Statement

Implement `solve(X, C, labels)`. Compute within-cluster sum of squared distances. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** Goldman Sachs is scenario context only; this is not an official Goldman Sachs interview question or endorsement.

### Example 1

**Input**

```python
solve([[0, 0], [2, 0], [9, 0]], [[0, 0], [10, 0]], [0, 0, 1])
```

**Output**

```text
5.0
```

**Explanation.** Compute within-cluster sum of squared distances.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
245.0
```

### Hint

sum point-to-centroid squared distances

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is K-Means Inertia?

Compute within-cluster sum of squared distances. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

K-Means Inertia supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **sum point-to-centroid squared distances**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `float(sum((np.sum((X[labels == k] - C[k]) ** 2) for k in range(len(C)))))`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([[0,0],[2,0],[9,0]],[[0,0],[10,0]],[0,0,1])` returns `5.0`. Reversing its observation rows returns `245.0`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`, `np.sum`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `float(sum((np.sum((X[labels == k] - C[k]) ** 2) for k in range(len(C)))))` after preparing the intermediates for K-Means Inertia. `np.asarray`, `np.sum` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
