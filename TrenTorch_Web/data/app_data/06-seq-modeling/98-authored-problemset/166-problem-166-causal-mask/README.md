---
name: problem-166-causal-mask
title: Causal Mask
tags: [sequence-models-attention, direct, hard, attention-mechanism.]
difficulty: Advanced
---

## Statement

Implement `solve(n)`. Implement the causal mask operation. Return only the specified value, preserving its shape and deterministic tie behavior.

### Example 1

**Input**

```python
solve(3)
```

**Output**

```text
[[True, False, False], [True, True, False], [True, True, True]]
```

**Explanation.** Implement the causal mask operation.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
[[True, False, False], [True, True, False], [True, True, True]]
```

### Hint

use indices i>=j

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Causal Mask?

Implement the causal mask operation. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Causal Mask supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **use indices i>=j**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `i >= j`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `(3,)` returns `[[True, False, False], [True, True, False], [True, True, True]]`. Reversing its observation rows returns `[[True, False, False], [True, True, False], [True, True, True]]`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.arange`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `i >= j` after preparing the intermediates for Causal Mask. `np.arange` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
