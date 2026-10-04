---
name: problem-54-elastic-net-penalty
title: Elastic-Net Penalty
tags: [classical-ml, case-study, medium, regularization., company-case]
difficulty: Intermediate
---

## Statement

Implement `solve(w, l1, l2)`. Compute the elastic-net penalty from a weight vector. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** Databricks is scenario context only; this is not an official Databricks interview question or endorsement.

### Example 1

**Input**

```python
solve([1, -2, 0], 0.1, 0.2)
```

**Output**

```text
0.8
```

**Explanation.** Compute the elastic-net penalty from a weight vector.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
0.6000000000000001
```

### Hint

combine L1 and L2 terms

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Elastic-Net Penalty?

Compute the elastic-net penalty from a weight vector. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Elastic-Net Penalty supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **combine L1 and L2 terms**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `float(l1 * np.sum(np.abs(w)) + 0.5 * l2 * np.sum(w * w))`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([1,-2,0],.1,.2)` returns `0.8`. Reversing its observation rows returns `0.6000000000000001`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.abs`, `np.asarray`, `np.sum`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `float(l1 * np.sum(np.abs(w)) + 0.5 * l2 * np.sum(w * w))` after preparing the intermediates for Elastic-Net Penalty. `np.abs`, `np.asarray`, `np.sum` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
