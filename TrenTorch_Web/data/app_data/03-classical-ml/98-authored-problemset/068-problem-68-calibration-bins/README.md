---
name: problem-68-calibration-bins
title: Calibration Bins
tags: [classical-ml, direct, medium, model-evaluation.]
difficulty: Intermediate
---

## Statement

Implement `solve(y, p, bins=10)`. Implement the calibration bins operation. Return only the specified value, preserving its shape and deterministic tie behavior.

### Example 1

**Input**

```python
solve([0, 1, 1, 0], [0.05, 0.2, 0.7, 0.95], 2)
```

**Output**

```text
[(0.125, 0.5, 2), (0.825, 0.5, 2)]
```

**Explanation.** Implement the calibration bins operation.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
[(0.125, 0.5, 2), (0.825, 0.5, 2)]
```

### Hint

bucket probabilities and compare mean confidence with event rate

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Calibration Bins?

Implement the calibration bins operation. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Calibration Bins supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **bucket probabilities and compare mean confidence with event rate**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `out`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([0,1,1,0],[.05,.2,.7,.95],2)` returns `[(0.125, 0.5, 2), (0.825, 0.5, 2)]`. Reversing its observation rows returns `[(0.125, 0.5, 2), (0.825, 0.5, 2)]`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.any`, `np.asarray`, `np.linspace`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `out` after preparing the intermediates for Calibration Bins. `np.any`, `np.asarray`, `np.linspace` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
