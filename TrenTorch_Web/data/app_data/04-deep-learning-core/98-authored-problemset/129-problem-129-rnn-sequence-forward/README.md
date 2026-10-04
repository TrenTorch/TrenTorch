---
name: problem-129-rnn-sequence-forward
title: RNN Sequence Forward
tags: [dl-core, case-study, hard, rnn-basics., company-case]
difficulty: Advanced
---

## Statement

Implement `solve(X, h0, Wx, Wh, b)`. Implement the rnn sequence forward operation. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** DoorDash is scenario context only; this is not an official DoorDash interview question or endorsement.

### Example 1

**Input**

```python
solve([[1], [2], [0]], [0], [[1]], [[0.5]], [0])
```

**Output**

```text
[[0.7615941559557649], [0.9830411011980433], [0.45542244071300725]]
```

**Explanation.** Implement the rnn sequence forward operation.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
[[0.0], [0.9640275800758169], [0.901844598209524]]
```

### Hint

carry hidden state across time

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is RNN Sequence Forward?

Implement the rnn sequence forward operation. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

RNN Sequence Forward supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **carry hidden state across time**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `np.asarray(states)`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([[1],[2],[0]],[0],[[1]],[[.5]],[0])` returns `[[0.7615941559557649], [0.9830411011980433], [0.45542244071300725]]`. Reversing its observation rows returns `[[0.0], [0.9640275800758169], [0.901844598209524]]`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`, `np.tanh`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `np.asarray(states)` after preparing the intermediates for RNN Sequence Forward. `np.asarray`, `np.tanh` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
