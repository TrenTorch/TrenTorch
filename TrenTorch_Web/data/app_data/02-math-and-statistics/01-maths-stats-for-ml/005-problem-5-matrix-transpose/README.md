---
name: problem-5-matrix-transpose
title: Matrix Transpose
tags: [maths-stats-for-ml, direct, medium, linear-algebra.]
difficulty: Intermediate
---

## Statement

Implement `solve(A)`. Return the transpose of a rectangular matrix. Return only the specified value, preserving its shape and deterministic tie behavior.

### Example 1

**Input**

```python
solve([[1, 2, 3], [4, 5, 6]])
```

**Output**

```text
[[1, 4], [2, 5], [3, 6]]
```

**Explanation.** Return the transpose of a rectangular matrix.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
[[4, 1], [5, 2], [6, 3]]
```

### Hint

swap row and column indices

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Matrix Transpose?

Return the transpose of a rectangular matrix. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Matrix Transpose supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **swap row and column indices**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `A.T`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([[1,2,3],[4,5,6]],)` returns `[[1, 4], [2, 5], [3, 6]]`. Reversing its observation rows returns `[[4, 1], [5, 2], [6, 3]]`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `A.T` after preparing the intermediates for Matrix Transpose. `np.asarray` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
