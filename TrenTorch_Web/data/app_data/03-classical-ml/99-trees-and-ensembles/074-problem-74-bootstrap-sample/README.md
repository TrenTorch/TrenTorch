---
name: problem-74-bootstrap-sample
title: Bootstrap Sample
tags: [classical-ml-trees-ensembles, case-study, easy, bagging., company-case]
difficulty: Beginner
---

## Statement

Implement `solve(n, seed=0)`. Draw N indices with replacement from N training examples. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** Flipkart is scenario context only; this is not an official Flipkart interview question or endorsement.

### Example 1

**Input**

```python
solve(5, 7)
```

**Output**

```text
[4, 3, 3, 4, 2]
```

**Explanation.** Draw N indices with replacement from N training examples.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
[4, 3, 3, 4, 2]
```

### Hint

use a seeded RNG

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Bootstrap Sample?

Draw N indices with replacement from N training examples. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Bootstrap Sample supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **use a seeded RNG**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `rng.integers(0, n, size=n)`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `(5,7)` returns `[4, 3, 3, 4, 2]`. Reversing its observation rows returns `[4, 3, 3, 4, 2]`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.random.default_rng`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `rng.integers(0, n, size=n)` after preparing the intermediates for Bootstrap Sample. `np.random.default_rng` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
