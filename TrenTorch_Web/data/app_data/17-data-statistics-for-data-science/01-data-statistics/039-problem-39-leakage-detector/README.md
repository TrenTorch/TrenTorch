---
name: problem-39-leakage-detector
title: Leakage Detector
tags: [data-stats-for-ds, case-study, easy, data-leakage., company-case]
difficulty: Beginner
---

## Statement

Implement `solve(columns)`. Implement the leakage detector operation. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** Tesla is scenario context only; this is not an official Tesla interview question or endorsement.

### Example 1

**Input**

```python
solve(['id', 'target', 'event_time', 'future_revenue', 'post_click', 'label_flag', 'safe'])
```

**Output**

```text
['target', 'future_revenue', 'post_click', 'label_flag']
```

**Explanation.** Implement the leakage detector operation.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
['label_flag', 'post_click', 'future_revenue', 'target']
```

### Hint

flag names matching a supplied forbidden pattern list

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Leakage Detector?

Implement the leakage detector operation. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Leakage Detector supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **flag names matching a supplied forbidden pattern list**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `[c for c in columns if any((k in c.lower() for k in forbidden))]`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `(['id','target','event_time','future_revenue','post_click','label_flag','safe'],)` returns `['target', 'future_revenue', 'post_click', 'label_flag']`. Reversing its observation rows returns `['label_flag', 'post_click', 'future_revenue', 'target']`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses Python arithmetic/iteration. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `[c for c in columns if any((k in c.lower() for k in forbidden))]` after preparing the intermediates for Leakage Detector. Python arithmetic/iteration directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
