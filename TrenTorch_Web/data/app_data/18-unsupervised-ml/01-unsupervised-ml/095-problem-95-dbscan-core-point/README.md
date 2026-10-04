---
name: problem-95-dbscan-core-point
title: DBSCAN Core Point
tags: [unsupervised-ml, case-study, hard, dbscan., company-case]
difficulty: Advanced
---

## Statement

Implement `solve(X, i, eps, min_samples=1)`. Determine whether a point has at least min_samples neighbors within eps. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** Tesla is scenario context only; this is not an official Tesla interview question or endorsement.

### Example 1

**Input**

```python
solve([[0], [1], [3], [8]], 1, 0.1, 2)
```

**Output**

```text
0
```

**Explanation.** Determine whether a point has at least min_samples neighbors within eps.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
0
```

### Hint

count neighbors including the point

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is DBSCAN Core Point?

Determine whether a point has at least min_samples neighbors within eps. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

DBSCAN Core Point supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **count neighbors including the point**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `int(np.sum(d <= eps ** 2) >= min_samples)`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([[0],[1],[3],[8]],1,.1,2)` returns `0`. Reversing its observation rows returns `0`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`, `np.sum`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `int(np.sum(d <= eps ** 2) >= min_samples)` after preparing the intermediates for DBSCAN Core Point. `np.asarray`, `np.sum` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
