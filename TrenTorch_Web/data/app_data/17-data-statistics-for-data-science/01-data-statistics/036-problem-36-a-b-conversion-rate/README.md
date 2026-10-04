---
name: problem-36-a-b-conversion-rate
title: A/B Conversion Rate
tags: [data-stats-for-ds, case-study, hard, ab-testing., company-case]
difficulty: Advanced
---

## Statement

Implement `solve(control, treatment)`. Implement the a/b conversion rate operation. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** Goldman Sachs is scenario context only; this is not an official Goldman Sachs interview question or endorsement.

### Example 1

**Input**

```python
solve([0, 1, 1, 0], [1, 1, 1, 0])
```

**Output**

```text
(0.5, 0.75, 0.25)
```

**Explanation.** Implement the a/b conversion rate operation.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
(0.5, 0.75, 0.25)
```

### Hint

count successes divided by group size

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is A/B Conversion Rate?

Implement the a/b conversion rate operation. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

A/B Conversion Rate supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **count successes divided by group size**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `(cr_a, cr_b, cr_b - cr_a)`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([0,1,1,0],[1,1,1,0])` returns `(0.5, 0.75, 0.25)`. Reversing its observation rows returns `(0.5, 0.75, 0.25)`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`, `np.mean`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `(cr_a, cr_b, cr_b - cr_a)` after preparing the intermediates for A/B Conversion Rate. `np.asarray`, `np.mean` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
