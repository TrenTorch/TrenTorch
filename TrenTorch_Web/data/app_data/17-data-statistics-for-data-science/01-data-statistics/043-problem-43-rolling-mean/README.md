---
name: problem-43-rolling-mean
title: Rolling Mean
tags: [data-stats-for-ds, direct, medium, time-series.]
difficulty: Intermediate
---

## Statement

Implement `solve(x, window)`. Compute a fixed-width trailing mean without using pandas. Return only the specified value, preserving its shape and deterministic tie behavior.

### Example 1

**Input**

```python
solve([1, 2, 3, 4, 5], 3)
```

**Output**

```text
[nan, nan, 2.0, 3.0, 4.0]
```

**Explanation.** Compute a fixed-width trailing mean without using pandas.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
[nan, nan, 4.0, 3.0, 2.0]
```

### Hint

maintain a running sum and remove the value leaving the window

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Rolling Mean?

Compute a fixed-width trailing mean without using pandas. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Rolling Mean supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **maintain a running sum and remove the value leaving the window**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `out`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([1,2,3,4,5],3)` returns `[nan, nan, 2.0, 3.0, 4.0]`. Reversing its observation rows returns `[nan, nan, 4.0, 3.0, 2.0]`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`, `np.full`, `np.nan`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `out` after preparing the intermediates for Rolling Mean. `np.asarray`, `np.full`, `np.nan` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
