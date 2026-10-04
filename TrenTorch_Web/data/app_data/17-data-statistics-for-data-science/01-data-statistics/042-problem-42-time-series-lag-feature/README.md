---
name: problem-42-time-series-lag-feature
title: Time-Series Lag Feature
tags: [data-stats-for-ds, case-study, medium, time-series., company-case]
difficulty: Intermediate
---

## Statement

Implement `solve(x)`. Create a one-step lag feature for a time-ordered series. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** Meesho is scenario context only; this is not an official Meesho interview question or endorsement.

### Example 1

**Input**

```python
solve([10, 20, 30])
```

**Output**

```text
[nan, 10.0, 20.0]
```

**Explanation.** Create a one-step lag feature for a time-ordered series.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
[nan, 30.0, 20.0]
```

### Hint

shift values right and mark the first row missing

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Time-Series Lag Feature?

Create a one-step lag feature for a time-ordered series. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Time-Series Lag Feature supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **shift values right and mark the first row missing**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `out`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([10,20,30],)` returns `[nan, 10.0, 20.0]`. Reversing its observation rows returns `[nan, 30.0, 20.0]`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`, `np.empty`, `np.nan`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `out` after preparing the intermediates for Time-Series Lag Feature. `np.asarray`, `np.empty`, `np.nan` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
