---
name: problem-193-greedy-decoding
title: Greedy Decoding
tags: [transformer-llm, case-study, easy, generation., company-case]
difficulty: Beginner
---

## Statement

Implement `solve(logits)`. Generate a sequence by repeatedly selecting the highest-probability token. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** NVIDIA is scenario context only; this is not an official NVIDIA interview question or endorsement.

### Example 1

**Input**

```python
solve([1, 5, 2])
```

**Output**

```text
1
```

**Explanation.** Generate a sequence by repeatedly selecting the highest-probability token.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
1
```

### Hint

argmax at every step

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Greedy Decoding?

Generate a sequence by repeatedly selecting the highest-probability token. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Greedy Decoding supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **argmax at every step**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `int(np.argmax(logits))`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([1,5,2],)` returns `1`. Reversing its observation rows returns `1`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.argmax`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `int(np.argmax(logits))` after preparing the intermediates for Greedy Decoding. `np.argmax` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
