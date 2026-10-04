---
name: problem-198-in-context-majority-vote
title: In-Context Majority Vote
tags: [transformer-llm, case-study, medium, in-context-learning., company-case]
difficulty: Intermediate
---

## Statement

Implement `solve(labels)`. Implement the in-context majority vote operation. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** Dropbox is scenario context only; this is not an official Dropbox interview question or endorsement.

### Example 1

**Input**

```python
solve(['a', 'b', 'a', 'c', 'a'])
```

**Output**

```text
'a'
```

**Explanation.** Implement the in-context majority vote operation.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
'a'
```

### Hint

count labels in the demonstrations

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is In-Context Majority Vote?

Implement the in-context majority vote operation. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

In-Context Majority Vote supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **count labels in the demonstrations**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `u[np.argmax(c)]`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `(['a','b','a','c','a'],)` returns `'a'`. Reversing its observation rows returns `'a'`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.argmax`, `np.unique`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `u[np.argmax(c)]` after preparing the intermediates for In-Context Majority Vote. `np.argmax`, `np.unique` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
