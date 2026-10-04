---
name: problem-29-iqr-outlier-flagging
title: IQR Outlier Flagging
tags: [data-stats-for-ds, case-study, medium, eda., company-case]
difficulty: Intermediate
---

## Statement

Implement `solve(x)`. Implement the iqr outlier flagging operation. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** Pinterest is scenario context only; this is not an official Pinterest interview question or endorsement.

### Example 1

**Input**

```python
solve([1, 2, 2, 3, 100])
```

**Output**

```text
[False, False, False, False, True]
```

**Explanation.** Implement the iqr outlier flagging operation.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
[True, False, False, False, False]
```

### Hint

compute Q1 and Q3 and compare bounds

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is IQR Outlier Flagging?

Implement the iqr outlier flagging operation. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

IQR Outlier Flagging supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **compute Q1 and Q3 and compare bounds**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `(x < q1 - 1.5 * iqr) | (x > q3 + 1.5 * iqr)`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([1,2,2,3,100],)` returns `[False, False, False, False, True]`. Reversing its observation rows returns `[True, False, False, False, False]`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`, `np.quantile`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `(x < q1 - 1.5 * iqr) | (x > q3 + 1.5 * iqr)` after preparing the intermediates for IQR Outlier Flagging. `np.asarray`, `np.quantile` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
