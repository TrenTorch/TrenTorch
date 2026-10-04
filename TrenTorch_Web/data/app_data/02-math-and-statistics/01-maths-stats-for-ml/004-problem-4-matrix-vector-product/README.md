---
name: problem-4-matrix-vector-product
title: Matrix-Vector Product
tags: [maths-stats-for-ml, direct, easy, linear-algebra.]
difficulty: Beginner
---

## Statement

Implement `solve(A, x)`. Implement multiplication of an m×n matrix by an n-vector from scratch. Return only the specified value, preserving its shape and deterministic tie behavior.

### Example 1

**Input**

```python
solve([[1, 2], [3, 4]], [2, 1])
```

**Output**

```text
[4.0, 10.0]
```

**Explanation.** Implement multiplication of an m×n matrix by an n-vector from scratch.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
[11.0, 5.0]
```

### Hint

accumulate one dot product per output row

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Matrix-Vector Product?

Implement multiplication of an m×n matrix by an n-vector from scratch. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Matrix-Vector Product supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **accumulate one dot product per output row**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `np.array([row @ x for row in A])`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([[1,2],[3,4]],[2,1])` returns `[4.0, 10.0]`. Reversing its observation rows returns `[11.0, 5.0]`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.array`, `np.asarray`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `np.array([row @ x for row in A])` after preparing the intermediates for Matrix-Vector Product. `np.array`, `np.asarray` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
