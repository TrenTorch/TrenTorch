---
name: problem-188-masked-lm-labels
title: Masked LM Labels
tags: [transformer-llm, direct, medium, pretraining-objectives.]
difficulty: Intermediate
---

## Statement

Implement `solve(ids, mask, ignore_index=-100)`. Implement the masked lm labels operation. Return only the specified value, preserving its shape and deterministic tie behavior.

### Example 1

**Input**

```python
solve([10, 11, 12, 13], [False, True, False, True])
```

**Output**

```text
([10, 11, 12, 13], [-100, 11, -100, 13])
```

**Explanation.** Implement the masked lm labels operation.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
([13, 12, 11, 10], [13, -100, 11, -100])
```

### Hint

use ignore index elsewhere

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Masked LM Labels?

Implement the masked lm labels operation. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Masked LM Labels supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **use ignore index elsewhere**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `(ids, labels)`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([10,11,12,13],[False,True,False,True])` returns `([10, 11, 12, 13], [-100, 11, -100, 13])`. Reversing its observation rows returns `([13, 12, 11, 10], [13, -100, 11, -100])`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`, `np.full_like`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `(ids, labels)` after preparing the intermediates for Masked LM Labels. `np.asarray`, `np.full_like` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
