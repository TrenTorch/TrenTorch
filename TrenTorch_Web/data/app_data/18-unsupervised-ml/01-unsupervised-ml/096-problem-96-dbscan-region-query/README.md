---
name: problem-96-dbscan-region-query
title: DBSCAN Region Query
tags: [unsupervised-ml, case-study, hard, dbscan., company-case]
difficulty: Advanced
---

## Statement

Implement `solve(X, i, eps)`. Implement the dbscan region query operation. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** Waymo is scenario context only; this is not an official Waymo interview question or endorsement.

### Example 1

**Input**

```python
solve([[0], [1], [3], [8]], 1, 2)
```

**Output**

```text
[0, 1, 2]
```

**Explanation.** Implement the dbscan region query operation.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
[1, 2]
```

### Hint

compare squared Euclidean distances

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is DBSCAN Region Query?

Implement the dbscan region query operation. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

DBSCAN Region Query supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **compare squared Euclidean distances**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `np.where(d <= eps ** 2)[0]`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([[0],[1],[3],[8]],1,2)` returns `[0, 1, 2]`. Reversing its observation rows returns `[1, 2]`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`, `np.sum`, `np.where`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `np.where(d <= eps ** 2)[0]` after preparing the intermediates for DBSCAN Region Query. `np.asarray`, `np.sum`, `np.where` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
