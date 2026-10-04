---
name: problem-152-transfer-learning-freeze
title: Transfer Learning Freeze
tags: [dl-training-theory, case-study, medium, transfer-learning., company-case]
difficulty: Intermediate
---

## Statement

Implement `solve(backbone, head)`. Mark backbone parameters frozen while leaving a head trainable. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** Waymo is scenario context only; this is not an official Waymo interview question or endorsement.

### Example 1

**Input**

```python
solve([Param(True), Param(False)], [Param(False)])
```

**Output**

```text
([Param(requires_grad=False), Param(requires_grad=False)], [Param(requires_grad=True)])
```

**Explanation.** Mark backbone parameters frozen while leaving a head trainable.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
([Param(requires_grad=False), Param(requires_grad=False)], [Param(requires_grad=True)])
```

### Hint

set requires_grad flags appropriately

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Transfer Learning Freeze?

Mark backbone parameters frozen while leaving a head trainable. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Transfer Learning Freeze supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **set requires_grad flags appropriately**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `(list(backbone), list(head))`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([Param(True),Param(False)],[Param(False)])` returns `([Param(requires_grad=False), Param(requires_grad=False)], [Param(requires_grad=True)])`. Reversing its observation rows returns `([Param(requires_grad=False), Param(requires_grad=False)], [Param(requires_grad=True)])`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses Python arithmetic/iteration. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `(list(backbone), list(head))` after preparing the intermediates for Transfer Learning Freeze. Python arithmetic/iteration directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
