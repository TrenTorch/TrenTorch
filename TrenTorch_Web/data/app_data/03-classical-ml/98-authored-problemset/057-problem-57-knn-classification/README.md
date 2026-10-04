---
name: problem-57-knn-classification
title: KNN Classification
tags: [classical-ml, case-study, hard, knn., company-case]
difficulty: Advanced
---

## Statement

Implement `solve(X, labels, q, k)`. Implement the knn classification operation. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** Netflix is scenario context only; this is not an official Netflix interview question or endorsement.

### Example 1

**Input**

```python
solve([[0], [1], [3], [4]], ['a', 'a', 'b', 'b'], [0.2], 3)
```

**Output**

```text
'a'
```

**Explanation.** Implement the knn classification operation.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
'a'
```

### Hint

use squared Euclidean distance and deterministic tie-breaking

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is KNN Classification?

Implement the knn classification operation. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

KNN Classification supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **use squared Euclidean distance and deterministic tie-breaking**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `u[np.argmax(c)]`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([[0],[1],[3],[4]],['a','a','b','b'],[.2],3)` returns `'a'`. Reversing its observation rows returns `'a'`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.argmax`, `np.argsort`, `np.asarray`, `np.sum`, `np.unique`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `u[np.argmax(c)]` after preparing the intermediates for KNN Classification. `np.argmax`, `np.argsort`, `np.asarray`, `np.sum`, `np.unique` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
