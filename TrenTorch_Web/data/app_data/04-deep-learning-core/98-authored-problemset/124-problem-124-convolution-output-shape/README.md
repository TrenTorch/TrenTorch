---
name: problem-124-convolution-output-shape
title: Convolution Output Shape
tags: [dl-core, direct, easy, cnn-basics.]
difficulty: Beginner
---

## Statement

Implement `solve(W, K, P, S)`. Compute 2D convolution output dimensions. Return only the specified value, preserving its shape and deterministic tie behavior.

### Example 1

**Input**

```python
solve(32, 3, 1, 2)
```

**Output**

```text
16
```

**Explanation.** Compute 2D convolution output dimensions.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
16
```

### Hint

apply floor((W+2P-K)/S)+1

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Convolution Output Shape?

Compute 2D convolution output dimensions. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Convolution Output Shape supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **apply floor((W+2P-K)/S)+1**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `(W + 2 * P - K) // S + 1`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `(32,3,1,2)` returns `16`. Reversing its observation rows returns `16`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses Python arithmetic/iteration. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `(W + 2 * P - K) // S + 1` after preparing the intermediates for Convolution Output Shape. Python arithmetic/iteration directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
