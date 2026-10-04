---
name: problem-6-frobenius-norm
title: Frobenius Norm
tags: [maths-stats-for-ml, case-study, medium, linear-algebra., company-case]
difficulty: Intermediate
---

## Statement

Implement `solve(x)`. Implement the frobenius norm operation. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** Amazon is scenario context only; this is not an official Amazon interview question or endorsement.

### Example 1

**Input**

```python
solve([[3, 4], [0, 0]])
```

**Output**

```text
5.0
```

**Explanation.** Implement the frobenius norm operation.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
5.0
```

### Hint

sum squared entries before taking one square root

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Frobenius Norm?

Implement the frobenius norm operation. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Frobenius Norm supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **sum squared entries before taking one square root**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `float(np.sqrt(np.sum(x * x)))`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([[3,4],[0,0]],)` returns `5.0`. Reversing its observation rows returns `5.0`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`, `np.sqrt`, `np.sum`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `float(np.sqrt(np.sum(x * x)))` after preparing the intermediates for Frobenius Norm. `np.asarray`, `np.sqrt`, `np.sum` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
