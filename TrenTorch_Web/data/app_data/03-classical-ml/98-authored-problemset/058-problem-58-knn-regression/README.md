---
name: problem-58-knn-regression
title: KNN Regression
tags: [classical-ml, case-study, hard, knn., company-case]
difficulty: Advanced
---

## Statement

Implement `solve(X, y, q, k)`. Implement the knn regression operation. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** Uber is scenario context only; this is not an official Uber interview question or endorsement.

### Example 1

**Input**

```python
solve([[0], [1], [3], [4]], [0, 2, 6, 8], [0.2], 2)
```

**Output**

```text
1.0
```

**Explanation.** Implement the knn regression operation.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
1.0
```

### Hint

average the neighbor targets

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is KNN Regression?

Implement the knn regression operation. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

KNN Regression supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **average the neighbor targets**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `float(np.mean(np.asarray(y)[np.argsort(d)[:k]]))`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([[0],[1],[3],[4]],[0,2,6,8],[.2],2)` returns `1.0`. Reversing its observation rows returns `1.0`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.argsort`, `np.asarray`, `np.mean`, `np.sum`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `float(np.mean(np.asarray(y)[np.argsort(d)[:k]]))` after preparing the intermediates for KNN Regression. `np.argsort`, `np.asarray`, `np.mean`, `np.sum` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
