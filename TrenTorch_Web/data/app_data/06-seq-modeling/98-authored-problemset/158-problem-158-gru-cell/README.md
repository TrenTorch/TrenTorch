---
name: problem-158-gru-cell
title: GRU Cell
tags: [sequence-models-attention, case-study, easy, rnn-lstm-gru., company-case]
difficulty: Beginner
---

## Statement

Implement `solve(x, h, W, b, Wh, bh)`. Implement the gru cell operation. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** CRED is scenario context only; this is not an official CRED interview question or endorsement.

### Example 1

**Input**

```python
solve([1], [0], np.zeros((2, 2)), [0, 0], np.zeros((1, 2)), [0])
```

**Output**

```text
[0.0]
```

**Explanation.** Implement the gru cell operation.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
[0.0]
```

### Hint

compute update and reset gates

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is GRU Cell?

Implement the gru cell operation. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

GRU Cell supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **compute update and reset gates**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `(1 - u) * h + u * htilde`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([1],[0],np.zeros((2,2)),[0,0],np.zeros((1,2)),[0])` returns `[0.0]`. Reversing its observation rows returns `[0.0]`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`, `np.exp`, `np.r_`, `np.split`, `np.tanh`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `(1 - u) * h + u * htilde` after preparing the intermediates for GRU Cell. `np.asarray`, `np.exp`, `np.r_`, `np.split`, `np.tanh` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
