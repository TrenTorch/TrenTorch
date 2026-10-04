---
name: problem-93-hierarchical-single-link-distance
title: Hierarchical Single-Link Distance
tags: [unsupervised-ml, case-study, hard, hierarchical-clustering., company-case]
difficulty: Advanced
---

## Statement

Implement `solve(A, B)`. Compute distance between two clusters using minimum pairwise distance. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** Coinbase is scenario context only; this is not an official Coinbase interview question or endorsement.

### Example 1

**Input**

```python
solve([[0, 0], [10, 0]], [[1, 0], [12, 0]])
```

**Output**

```text
1.0
```

**Explanation.** Compute distance between two clusters using minimum pairwise distance.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
1.0
```

### Hint

take the minimum cross-cluster distance

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Hierarchical Single-Link Distance?

Compute distance between two clusters using minimum pairwise distance. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Hierarchical Single-Link Distance supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **take the minimum cross-cluster distance**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `float(np.min(np.sqrt(((A[:, None] - B[None, :]) ** 2).sum(2))))`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([[0,0],[10,0]],[[1,0],[12,0]])` returns `1.0`. Reversing its observation rows returns `1.0`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`, `np.min`, `np.sqrt`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `float(np.min(np.sqrt(((A[:, None] - B[None, :]) ** 2).sum(2))))` after preparing the intermediates for Hierarchical Single-Link Distance. `np.asarray`, `np.min`, `np.sqrt` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
