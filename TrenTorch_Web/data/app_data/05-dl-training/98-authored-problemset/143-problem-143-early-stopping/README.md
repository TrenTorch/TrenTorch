---
name: problem-143-early-stopping
title: Early Stopping
tags: [dl-training-theory, direct, hard, regularization.]
difficulty: Advanced
---

## Statement

Implement `solve(losses, patience)`. Track validation loss and stop after patience bad epochs. Return only the specified value, preserving its shape and deterministic tie behavior.

### Example 1

**Input**

```python
solve([5, 4, 4, 4], 2)
```

**Output**

```text
True
```

**Explanation.** Track validation loss and stop after patience bad epochs.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
True
```

### Hint

reset patience on strict improvement

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Early Stopping?

Track validation loss and stop after patience bad epochs. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Early Stopping supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **reset patience on strict improvement**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `False`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([5,4,4,4],2)` returns `True`. Reversing its observation rows returns `True`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses Python arithmetic/iteration. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `False` after preparing the intermediates for Early Stopping. Python arithmetic/iteration directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
