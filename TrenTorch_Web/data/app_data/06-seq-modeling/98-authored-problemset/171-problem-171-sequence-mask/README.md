---
name: problem-171-sequence-mask
title: Sequence Mask
tags: [sequence-models-attention, case-study, easy, sequence-masking., company-case]
difficulty: Beginner
---

## Statement

Implement `solve(ids, pad_id)`. Build a 0/1 mask for non-padding tokens. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** Google is scenario context only; this is not an official Google interview question or endorsement.

### Example 1

**Input**

```python
solve([1, 0, 2, 0], 0)
```

**Output**

```text
[1, 0, 1, 0]
```

**Explanation.** Build a 0/1 mask for non-padding tokens.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
[0, 1, 0, 1]
```

### Hint

compare token IDs to pad ID

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Sequence Mask?

Build a 0/1 mask for non-padding tokens. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Sequence Mask supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **compare token IDs to pad ID**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `(np.asarray(ids) != pad_id).astype(int)`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([1,0,2,0],0)` returns `[1, 0, 1, 0]`. Reversing its observation rows returns `[0, 1, 0, 1]`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `(np.asarray(ids) != pad_id).astype(int)` after preparing the intermediates for Sequence Mask. `np.asarray` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
