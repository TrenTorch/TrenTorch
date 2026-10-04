---
name: problem-150-mini-batch-iterator
title: Mini-Batch Iterator
tags: [dl-training-theory, case-study, medium, batch-dynamics., company-case]
difficulty: Intermediate
---

## Statement

Implement `solve(X, y, batch_size, seed=0)`. Yield shuffled mini-batches without dropping the remainder. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** Palantir is scenario context only; this is not an official Palantir interview question or endorsement.

### Example 1

**Input**

```python
solve([[1], [2], [3], [4]], [10, 20, 30, 40], 2, 3)
```

**Output**

```text
[([[4], [3]], [40, 30]), ([[2], [1]], [20, 10])]
```

**Explanation.** Yield shuffled mini-batches without dropping the remainder.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
[([[1], [2]], [10, 20]), ([[3], [4]], [30, 40])]
```

### Hint

permute indices once per epoch

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Mini-Batch Iterator?

Yield shuffled mini-batches without dropping the remainder. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Mini-Batch Iterator supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **permute indices once per epoch**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `[(X[j], y[j]) for j in np.array_split(idx, int(np.ceil(len(X) / batch_size)))]`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([[1],[2],[3],[4]],[10,20,30,40],2,3)` returns `[([[4], [3]], [40, 30]), ([[2], [1]], [20, 10])]`. Reversing its observation rows returns `[([[1], [2]], [10, 20]), ([[3], [4]], [30, 40])]`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.arange`, `np.array_split`, `np.asarray`, `np.ceil`, `np.random.default_rng`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `[(X[j], y[j]) for j in np.array_split(idx, int(np.ceil(len(X) / batch_size)))]` after preparing the intermediates for Mini-Batch Iterator. `np.arange`, `np.array_split`, `np.asarray`, `np.ceil`, `np.random.default_rng` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
