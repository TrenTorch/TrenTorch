---
name: problem-169-attention-padding-mask
title: Attention Padding Mask
tags: [sequence-models-attention, case-study, easy, sequence-padding., company-case]
difficulty: Beginner
---

## Statement

Implement `solve(ids, pad_id)`. Implement the attention padding mask operation. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** Netflix is scenario context only; this is not an official Netflix interview question or endorsement.

### Example 1

**Input**

```python
solve([1, 0, 2, 0], 0)
```

**Output**

```text
[True, False, True, False]
```

**Explanation.** Implement the attention padding mask operation.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
[False, True, False, True]
```

### Hint

broadcast a boolean mask over query positions

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Attention Padding Mask?

Implement the attention padding mask operation. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Attention Padding Mask supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **broadcast a boolean mask over query positions**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `np.asarray(ids) != pad_id`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([1,0,2,0],0)` returns `[True, False, True, False]`. Reversing its observation rows returns `[False, True, False, True]`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `np.asarray(ids) != pad_id` after preparing the intermediates for Attention Padding Mask. `np.asarray` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
