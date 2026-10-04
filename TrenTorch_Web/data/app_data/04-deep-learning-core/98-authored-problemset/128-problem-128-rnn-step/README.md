---
name: problem-128-rnn-step
title: RNN Step
tags: [dl-core, direct, medium, rnn-basics.]
difficulty: Intermediate
---

## Statement

Implement `solve(x, h, Wx, Wh, b)`. Implement the rnn step operation. Return only the specified value, preserving its shape and deterministic tie behavior.

### Example 1

**Input**

```python
solve([1, 2], [0], [[1, 1]], [[1]], [0])
```

**Output**

```text
[0.9950547536867305]
```

**Explanation.** Implement the rnn step operation.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
[0.9950547536867305]
```

### Hint

h=tanh(Wx+Uh_prev+b)

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is RNN Step?

Implement the rnn step operation. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

RNN Step supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **h=tanh(Wx+Uh_prev+b)**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `np.tanh(Wx @ x + Wh @ h + b)`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([1,2],[0],[[1,1]],[[1]],[0])` returns `[0.9950547536867305]`. Reversing its observation rows returns `[0.9950547536867305]`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`, `np.tanh`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `np.tanh(Wx @ x + Wh @ h + b)` after preparing the intermediates for RNN Step. `np.asarray`, `np.tanh` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
