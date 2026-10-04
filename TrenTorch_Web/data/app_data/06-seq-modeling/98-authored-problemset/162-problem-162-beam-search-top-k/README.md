---
name: problem-162-beam-search-top-k
title: Beam Search Top-K
tags: [sequence-models-attention, case-study, medium, beam-search., company-case]
difficulty: Intermediate
---

## Statement

Implement `solve(step_scores, k)`. Keep the k highest-scoring partial sequences. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** Zoom is scenario context only; this is not an official Zoom interview question or endorsement.

### Example 1

**Input**

```python
solve([[-0.1, -0.5], [-0.2, -0.3]], 2)
```

**Output**

```text
[([0, 0], -0.30000000000000004), ([0, 1], -0.4)]
```

**Explanation.** Keep the k highest-scoring partial sequences.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
[([0, 0], -0.30000000000000004), ([1, 0], -0.4)]
```

### Hint

expand candidates then sort by cumulative score

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Beam Search Top-K?

Keep the k highest-scoring partial sequences. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Beam Search Top-K supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **expand candidates then sort by cumulative score**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `beams`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([[-.1,-.5],[-.2,-.3]],2)` returns `[([0, 0], -0.30000000000000004), ([0, 1], -0.4)]`. Reversing its observation rows returns `[([0, 0], -0.30000000000000004), ([1, 0], -0.4)]`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses Python arithmetic/iteration. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `beams` after preparing the intermediates for Beam Search Top-K. Python arithmetic/iteration directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
