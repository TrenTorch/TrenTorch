---
name: problem-60-f1-score
title: F1 Score
tags: [classical-ml, case-study, hard, metrics., company-case]
difficulty: Advanced
---

## Statement

Implement `solve(precision, recall)`. Compute the harmonic mean of precision and recall. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** Microsoft is scenario context only; this is not an official Microsoft interview question or endorsement.

### Example 1

**Input**

```python
solve(0.75, 0.5)
```

**Output**

```text
0.6
```

**Explanation.** Compute the harmonic mean of precision and recall.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
0.45
```

### Hint

return zero when both are zero

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is F1 Score?

Compute the harmonic mean of precision and recall. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

F1 Score supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **return zero when both are zero**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `0.0 if p + r == 0 else 2 * p * r / (p + r)`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `(.75,.5)` returns `0.6`. Reversing its observation rows returns `0.45`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses Python arithmetic/iteration. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `0.0 if p + r == 0 else 2 * p * r / (p + r)` after preparing the intermediates for F1 Score. Python arithmetic/iteration directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
