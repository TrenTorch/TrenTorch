---
name: problem-110-relu-backward
title: ReLU Backward
tags: [dl-core, case-study, easy, activation-functions., company-case]
difficulty: Beginner
---

## Statement

Implement `solve(x)`. Compute the derivative mask of ReLU. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** Databricks is scenario context only; this is not an official Databricks interview question or endorsement.

### Example 1

**Input**

```python
solve([-2, 0, 3])
```

**Output**

```text
[0.0, 0.0, 1.0]
```

**Explanation.** Compute the derivative mask of ReLU.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
[1.0, 0.0, 0.0]
```

### Hint

return 1 where x>0 else 0

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is ReLU Backward?

Compute the derivative mask of ReLU. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

ReLU Backward supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **return 1 where x>0 else 0**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `(np.asarray(x) > 0).astype(float)`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([-2,0,3],)` returns `[0.0, 0.0, 1.0]`. Reversing its observation rows returns `[1.0, 0.0, 0.0]`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `(np.asarray(x) > 0).astype(float)` after preparing the intermediates for ReLU Backward. `np.asarray` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
