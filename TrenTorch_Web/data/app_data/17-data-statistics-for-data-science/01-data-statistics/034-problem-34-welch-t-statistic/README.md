---
name: problem-34-welch-t-statistic
title: Welch t Statistic
tags: [data-stats-for-ds, case-study, hard, hypothesis-testing., company-case]
difficulty: Advanced
---

## Statement

Implement `solve(a, b)`. Compute the Welch t-statistic for two independent samples. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** PayPal is scenario context only; this is not an official PayPal interview question or endorsement.

### Example 1

**Input**

```python
solve([1, 2, 3, 4], [2, 4, 6, 8])
```

**Output**

```text
-1.7320508075688772
```

**Explanation.** Compute the Welch t-statistic for two independent samples.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
-1.7320508075688772
```

### Hint

use unequal-variance standard error

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Welch t Statistic?

Compute the Welch t-statistic for two independent samples. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Welch t Statistic supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **use unequal-variance standard error**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `float((a.mean() - b.mean()) / np.sqrt(va / len(a) + vb / len(b)))`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([1,2,3,4],[2,4,6,8])` returns `-1.7320508075688772`. Reversing its observation rows returns `-1.7320508075688772`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`, `np.sqrt`, `np.var`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `float((a.mean() - b.mean()) / np.sqrt(va / len(a) + vb / len(b)))` after preparing the intermediates for Welch t Statistic. `np.asarray`, `np.sqrt`, `np.var` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
