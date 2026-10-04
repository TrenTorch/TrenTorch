---
name: problem-121-he-initialization
title: He Initialization
tags: [dl-core, direct, easy, weight-initialization.]
difficulty: Beginner
---

## Statement

Implement `solve(fan_in, fan_out, seed=0)`. Generate ReLU-layer weights with He normal initialization. Return only the specified value, preserving its shape and deterministic tie behavior.

### Example 1

**Input**

```python
solve(2, 3, 4)
```

**Output**

```text
[[-0.6517911526116896, -0.17471729232577715, 1.6637239913911968], [0.659147749832255, -1.6413972945846467, -0.005203264171931977]]
```

**Explanation.** Generate ReLU-layer weights with He normal initialization.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
[[-0.6517911526116896, -0.17471729232577715, 1.6637239913911968], [0.659147749832255, -1.6413972945846467, -0.005203264171931977]]
```

### Hint

std=sqrt(2/fan_in)

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is He Initialization?

Generate ReLU-layer weights with He normal initialization. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

He Initialization supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **std=sqrt(2/fan_in)**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `rng.normal(0, np.sqrt(2 / fan_in), (fan_in, fan_out))`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `(2,3,4)` returns `[[-0.6517911526116896, -0.17471729232577715, 1.6637239913911968], [0.659147749832255, -1.6413972945846467, -0.005203264171931977]]`. Reversing its observation rows returns `[[-0.6517911526116896, -0.17471729232577715, 1.6637239913911968], [0.659147749832255, -1.6413972945846467, -0.005203264171931977]]`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.random.default_rng`, `np.sqrt`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `rng.normal(0, np.sqrt(2 / fan_in), (fan_in, fan_out))` after preparing the intermediates for He Initialization. `np.random.default_rng`, `np.sqrt` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
