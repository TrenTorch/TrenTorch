---
name: problem-140-warmup-schedule
title: Warmup Schedule
tags: [dl-training-theory, direct, medium, learning-rate-schedules.]
difficulty: Intermediate
---

## Statement

Implement `solve(lr0, min_lr, t, warmup, T)`. Linearly warm learning rate before a cosine decay. Return only the specified value, preserving its shape and deterministic tie behavior.

### Example 1

**Input**

```python
solve(0.1, 0.01, 0, 3, 10)
```

**Output**

```text
0.03333333333333333
```

**Explanation.** Linearly warm learning rate before a cosine decay.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
0.025000000000000005
```

### Hint

piecewise warmup then cosine

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Warmup Schedule?

Linearly warm learning rate before a cosine decay. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Warmup Schedule supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **piecewise warmup then cosine**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `min_lr + 0.5 * (lr0 - min_lr) * (1 + np.cos(np.pi * q / max(1, T - warmup)))`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `(.1,.01,0,3,10)` returns `0.03333333333333333`. Reversing its observation rows returns `0.025000000000000005`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.cos`, `np.pi`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `min_lr + 0.5 * (lr0 - min_lr) * (1 + np.cos(np.pi * q / max(1, T - warmup)))` after preparing the intermediates for Warmup Schedule. `np.cos`, `np.pi` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
