---
name: problem-183-post-norm-transformer-block
title: Post-Norm Transformer Block
tags: [transformer-llm, case-study, easy, layer-norm-and-residuals., company-case]
difficulty: Beginner
---

## Statement

Implement `solve(x, norm, attention, ff)`. Apply layer normalization after each residual addition. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** Datadog is scenario context only; this is not an official Datadog interview question or endorsement.

### Example 1

**Input**

```python
solve([1.0, 2.0], lambda z: np.asarray(z), lambda z: np.asarray(z) * 2, lambda z: np.asarray(z) + 1)
```

**Output**

```text
[7.0, 13.0]
```

**Explanation.** Apply layer normalization after each residual addition.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
[13.0, 7.0]
```

### Hint

use post-norm ordering

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Post-Norm Transformer Block?

Apply layer normalization after each residual addition. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Post-Norm Transformer Block supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **use post-norm ordering**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `norm(y + ff(y))`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([1.,2.],lambda z:np.asarray(z),lambda z:np.asarray(z)*2,lambda z:np.asarray(z)+1)` returns `[7.0, 13.0]`. Reversing its observation rows returns `[13.0, 7.0]`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses Python arithmetic/iteration. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `norm(y + ff(y))` after preparing the intermediates for Post-Norm Transformer Block. Python arithmetic/iteration directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
