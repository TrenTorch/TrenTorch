---
name: problem-35-confidence-interval-for-mean
title: Confidence Interval for Mean
tags: [data-stats-for-ds, case-study, hard, confidence-intervals., company-case]
difficulty: Advanced
---

## Statement

Implement `solve(x, critical=1.96)`. Construct a normal-approximation confidence interval for a mean. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** JPMorgan Chase is scenario context only; this is not an official JPMorgan Chase interview question or endorsement.

### Example 1

**Input**

```python
solve([1, 2, 3, 4], 1.96)
```

**Output**

```text
(1.2348254402389105, 3.7651745597610895)
```

**Explanation.** Construct a normal-approximation confidence interval for a mean.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
(1.5511190801791828, 3.4488809198208172)
```

### Hint

mean ± critical_value*SE

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Confidence Interval for Mean?

Construct a normal-approximation confidence interval for a mean. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Confidence Interval for Mean supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **mean ± critical_value\*SE**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `(m - critical * se, m + critical * se)`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([1,2,3,4],1.96)` returns `(1.2348254402389105, 3.7651745597610895)`. Reversing its observation rows returns `(1.5511190801791828, 3.4488809198208172)`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`, `np.sqrt`, `np.std`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `(m - critical * se, m + critical * se)` after preparing the intermediates for Confidence Interval for Mean. `np.asarray`, `np.sqrt`, `np.std` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
