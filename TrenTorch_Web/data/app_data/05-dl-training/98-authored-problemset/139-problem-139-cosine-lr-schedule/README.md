---
name: problem-139-cosine-lr-schedule
title: Cosine LR Schedule
tags: [dl-training-theory, case-study, medium, learning-rate-schedules., company-case]
difficulty: Intermediate
---

## Statement

Implement `solve(lr_max, lr_min, t, T)`. Implement the cosine lr schedule operation. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** Salesforce is scenario context only; this is not an official Salesforce interview question or endorsement.

### Example 1

**Input**

```python
solve(0.1, 0.01, 0, 10)
```

**Output**

```text
0.1
```

**Explanation.** Implement the cosine lr schedule operation.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
0.07500000000000001
```

### Hint

use half-cosine interpolation

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Cosine LR Schedule?

Implement the cosine lr schedule operation. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Cosine LR Schedule supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **use half-cosine interpolation**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `float(lr_min + 0.5 * (lr_max - lr_min) * (1 + np.cos(np.pi * q / T)))`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `(.1,.01,0,10)` returns `0.1`. Reversing its observation rows returns `0.07500000000000001`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.cos`, `np.pi`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `float(lr_min + 0.5 * (lr_max - lr_min) * (1 + np.cos(np.pi * q / T)))` after preparing the intermediates for Cosine LR Schedule. `np.cos`, `np.pi` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
