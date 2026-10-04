---
name: problem-163-length-normalized-beam-search
title: Length-Normalized Beam Search
tags: [sequence-models-attention, direct, medium, beam-search.]
difficulty: Intermediate
---

## Statement

Implement `solve(beams, alpha)`. Rank beams using length-normalized log probability. Return only the specified value, preserving its shape and deterministic tie behavior.

### Example 1

**Input**

```python
solve([([1, 2], -2.0), ([3], -1.0)], 1.0)
```

**Output**

```text
([1, 2], -2.0)
```

**Explanation.** Rank beams using length-normalized log probability.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
([3], -1.0)
```

### Hint

divide score by length^alpha

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Length-Normalized Beam Search?

Rank beams using length-normalized log probability. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Length-Normalized Beam Search supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **divide score by length^alpha**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `max(beams, key=lambda z: z[1] / len(z[0]) ** alpha)`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([([1,2],-2.),([3],-1.)],1.)` returns `([1, 2], -2.0)`. Reversing its observation rows returns `([3], -1.0)`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses Python arithmetic/iteration. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `max(beams, key=lambda z: z[1] / len(z[0]) ** alpha)` after preparing the intermediates for Length-Normalized Beam Search. Python arithmetic/iteration directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
