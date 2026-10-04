---
name: problem-149-random-search-sampler
title: Random Search Sampler
tags: [dl-training-theory, case-study, medium, hyperparameter-tuning., company-case]
difficulty: Intermediate
---

## Statement

Implement `solve(n, seed=0)`. Implement the random search sampler operation. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** Coinbase is scenario context only; this is not an official Coinbase interview question or endorsement.

### Example 1

**Input**

```python
solve(3, 4)
```

**Output**

```text
[{'lr': 0.059186740348548664, 'depth': 9}, {'lr': 0.08034795410579068, 'depth': 6}, {'lr': 2.1054459436149825e-05, 'depth': 5}]
```

**Explanation.** Implement the random search sampler operation.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
[{'lr': 0.059186740348548664, 'depth': 9}, {'lr': 0.08034795410579068, 'depth': 6}, {'lr': 2.1054459436149825e-05, 'depth': 5}]
```

### Hint

use seeded random sampling

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Random Search Sampler?

Implement the random search sampler operation. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Random Search Sampler supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **use seeded random sampling**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `[{'lr': float(10 ** rng.uniform(-5, -1)), 'depth': int(rng.integers(2, 10))} for _ in range(n)]`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `(3,4)` returns `[{'lr': 0.059186740348548664, 'depth': 9}, {'lr': 0.08034795410579068, 'depth': 6}, {'lr': 2.1054459436149825e-05, 'depth': 5}]`. Reversing its observation rows returns `[{'lr': 0.059186740348548664, 'depth': 9}, {'lr': 0.08034795410579068, 'depth': 6}, {'lr': 2.1054459436149825e-05, 'depth': 5}]`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.random.default_rng`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `[{'lr': float(10 ** rng.uniform(-5, -1)), 'depth': int(rng.integers(2, 10))} for _ in range(n)]` after preparing the intermediates for Random Search Sampler. `np.random.default_rng` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
