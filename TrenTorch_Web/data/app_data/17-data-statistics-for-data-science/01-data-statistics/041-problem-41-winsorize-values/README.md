---
name: problem-41-winsorize-values
title: Winsorize Values
tags: [data-stats-for-ds, direct, medium, eda.]
difficulty: Intermediate
---

## Statement

Implement `solve(x, lower=0.05, upper=0.95)`. Clip a numeric vector to supplied lower and upper quantiles. Return only the specified value, preserving its shape and deterministic tie behavior.

### Example 1

**Input**

```python
solve([0, 1, 2, 3, 100], 0.2, 0.8)
```

**Output**

```text
[0.8, 1.0, 2.0, 3.0, 22.400000000000016]
```

**Explanation.** Clip a numeric vector to supplied lower and upper quantiles.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
[2.4000000000000004, 2.4000000000000004, 2.0, 1.0, 0.6000000000000001]
```

### Hint

compute quantiles and clip

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Winsorize Values?

Clip a numeric vector to supplied lower and upper quantiles. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Winsorize Values supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **compute quantiles and clip**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `np.clip(x, lo, hi)`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([0,1,2,3,100],.2,.8)` returns `[0.8, 1.0, 2.0, 3.0, 22.400000000000016]`. Reversing its observation rows returns `[2.4000000000000004, 2.4000000000000004, 2.0, 1.0, 0.6000000000000001]`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`, `np.clip`, `np.quantile`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `np.clip(x, lo, hi)` after preparing the intermediates for Winsorize Values. `np.asarray`, `np.clip`, `np.quantile` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
