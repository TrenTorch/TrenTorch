---
name: problem-32-bootstrap-mean
title: Bootstrap Mean
tags: [data-stats-for-ds, case-study, medium, sampling., company-case]
difficulty: Intermediate
---

## Statement

Implement `solve(x, B=1000, alpha=0.05, seed=0)`. Estimate a confidence interval for a sample mean with bootstrap resampling. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** Instacart is scenario context only; this is not an official Instacart interview question or endorsement.

### Example 1

**Input**

```python
solve([1, 2, 3, 4], 40, 0.1, 4)
```

**Output**

```text
(1.7375, 3.5)
```

**Explanation.** Estimate a confidence interval for a sample mean with bootstrap resampling.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
(1.5, 3.3843750000000004)
```

### Hint

resample rows with replacement and collect means

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Bootstrap Mean?

Estimate a confidence interval for a sample mean with bootstrap resampling. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Bootstrap Mean supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **resample rows with replacement and collect means**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `(float(np.quantile(means, alpha / 2)), float(np.quantile(means, 1 - alpha / 2)))`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([1,2,3,4],40,.1,4)` returns `(1.7375, 3.5)`. Reversing its observation rows returns `(1.5, 3.3843750000000004)`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`, `np.empty`, `np.mean`, `np.quantile`, `np.random.default_rng`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `(float(np.quantile(means, alpha / 2)), float(np.quantile(means, 1 - alpha / 2)))` after preparing the intermediates for Bootstrap Mean. `np.asarray`, `np.empty`, `np.mean`, `np.quantile`, `np.random.default_rng` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
