---
name: problem-191-top-p-sampling
title: Top-P Sampling
tags: [transformer-llm, case-study, hard, generation., company-case]
difficulty: Advanced
---

## Statement

Implement `solve(logits, p_cut, rng)`. Sample from the smallest probability prefix whose cumulative mass reaches p. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** ByteDance is scenario context only; this is not an official ByteDance interview question or endorsement.

### Example 1

**Input**

```python
solve([1, 2, 3, 0], 0.7, np.random.default_rng(7))
```

**Output**

```text
2
```

**Explanation.** Sample from the smallest probability prefix whose cumulative mass reaches p.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
1
```

### Hint

sort probabilities and truncate the tail

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Top-P Sampling?

Sample from the smallest probability prefix whose cumulative mass reaches p. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Top-P Sampling supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **sort probabilities and truncate the tail**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `rng.choice(len(z), p=q)`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([1,2,3,0],.7,np.random.default_rng(7))` returns `2`. Reversing its observation rows returns `1`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.argsort`, `np.asarray`, `np.cumsum`, `np.exp`, `np.r_`, `np.searchsorted`, `np.zeros_like`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `rng.choice(len(z), p=q)` after preparing the intermediates for Top-P Sampling. `np.argsort`, `np.asarray`, `np.cumsum`, `np.exp`, `np.r_`, `np.searchsorted`, `np.zeros_like` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
