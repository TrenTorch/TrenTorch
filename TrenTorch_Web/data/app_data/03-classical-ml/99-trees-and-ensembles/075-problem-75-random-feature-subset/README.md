---
name: problem-75-random-feature-subset
title: Random Feature Subset
tags: [classical-ml-trees-ensembles, case-study, easy, random-forest., company-case]
difficulty: Beginner
---

## Statement

Implement `solve(n_features, m, seed=0)`. Choose m features without replacement for a tree node. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** Swiggy is scenario context only; this is not an official Swiggy interview question or endorsement.

### Example 1

**Input**

```python
solve(8, 3, 4)
```

**Output**

```text
[4, 7, 6]
```

**Explanation.** Choose m features without replacement for a tree node.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
[4, 7, 6]
```

### Hint

sample feature indices from the available set

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Random Feature Subset?

Choose m features without replacement for a tree node. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Random Feature Subset supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **sample feature indices from the available set**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `rng.choice(n_features, size=m, replace=False)`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `(8,3,4)` returns `[4, 7, 6]`. Reversing its observation rows returns `[4, 7, 6]`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.random.default_rng`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `rng.choice(n_features, size=m, replace=False)` after preparing the intermediates for Random Feature Subset. `np.random.default_rng` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
