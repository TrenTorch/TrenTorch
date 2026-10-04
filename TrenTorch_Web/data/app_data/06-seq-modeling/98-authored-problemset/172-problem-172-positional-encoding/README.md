---
name: problem-172-positional-encoding
title: Positional Encoding
tags: [sequence-models-attention, case-study, easy, positional-encoding., company-case]
difficulty: Beginner
---

## Statement

Implement `solve(n, dim)`. Generate sinusoidal positional encodings. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** Microsoft is scenario context only; this is not an official Microsoft interview question or endorsement.

### Example 1

**Input**

```python
solve(4, 5)
```

**Output**

```text
[[0.0, 1.0, 0.0, 1.0, 0.0], [0.8414709848078965, 0.5403023058681398, 0.025116222909773774, 0.9996845379152098, 0.0006309573026154199], [0.9092974268256817, -0.4161468365471424, 0.050216599387465206, 0.9987383506934931, 0.0012619143540422218], [0.1411200080598672, -0.9899924966004454, 0.07528529299888893, 0.997162035307237, 0.0018928709030918874]]
```

**Explanation.** Generate sinusoidal positional encodings.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
[[0.0, 1.0, 0.0, 1.0, 0.0], [0.8414709848078965, 0.5403023058681398, 0.025116222909773774, 0.9996845379152098, 0.0006309573026154199], [0.9092974268256817, -0.4161468365471424, 0.050216599387465206, 0.9987383506934931, 0.0012619143540422218], [0.1411200080598672, -0.9899924966004454, 0.07528529299888893, 0.997162035307237, 0.0018928709030918874]]
```

### Hint

use sine on even dimensions and cosine on odd

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Positional Encoding?

Generate sinusoidal positional encodings. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Positional Encoding supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **use sine on even dimensions and cosine on odd**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `E`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `(4,5)` returns `[[0.0, 1.0, 0.0, 1.0, 0.0], [0.8414709848078965, 0.5403023058681398, 0.025116222909773774, 0.9996845379152098, 0.0006309573026154199], [0.9092974268256817, -0.4161468365471424, 0.050216599387465206, 0.9987383506934931, 0.0012619143540422218], [0.1411200080598672, -0.9899924966004454, 0.07528529299888893, 0.997162035307237, 0.0018928709030918874]]`. Reversing its observation rows returns `[[0.0, 1.0, 0.0, 1.0, 0.0], [0.8414709848078965, 0.5403023058681398, 0.025116222909773774, 0.9996845379152098, 0.0006309573026154199], [0.9092974268256817, -0.4161468365471424, 0.050216599387465206, 0.9987383506934931, 0.0012619143540422218], [0.1411200080598672, -0.9899924966004454, 0.07528529299888893, 0.997162035307237, 0.0018928709030918874]]`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.arange`, `np.cos`, `np.empty`, `np.power`, `np.sin`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `E` after preparing the intermediates for Positional Encoding. `np.arange`, `np.cos`, `np.empty`, `np.power`, `np.sin` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
