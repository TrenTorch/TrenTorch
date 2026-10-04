---
name: problem-24-median-imputation
title: Median Imputation
tags: [data-stats-for-ds, case-study, hard, data-cleaning., company-case]
difficulty: Advanced
---

## Statement

Implement `solve(x)`. Replace missing numeric entries with the observed-column median. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** TikTok is scenario context only; this is not an official TikTok interview question or endorsement.

### Example 1

**Input**

```python
solve([1, np.nan, 9])
```

**Output**

```text
[1.0, 5.0, 9.0]
```

**Explanation.** Replace missing numeric entries with the observed-column median.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
[9.0, 5.0, 1.0]
```

### Hint

sort the observed values or use np.median

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Median Imputation?

Replace missing numeric entries with the observed-column median. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Median Imputation supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **sort the observed values or use np.median**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `x`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([1,np.nan,9],)` returns `[1.0, 5.0, 9.0]`. Reversing its observation rows returns `[9.0, 5.0, 1.0]`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`, `np.isnan`, `np.nanmedian`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `x` after preparing the intermediates for Median Imputation. `np.asarray`, `np.isnan`, `np.nanmedian` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
