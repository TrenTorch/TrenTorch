---
name: problem-196-lora-parameter-count
title: LoRA Parameter Count
tags: [transformer-llm, case-study, easy, fine-tuning-and-peft., company-case]
difficulty: Beginner
---

## Statement

Implement `solve(in_features, out_features, r)`. Implement the lora parameter count operation. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** Shopify is scenario context only; this is not an official Shopify interview question or endorsement.

### Example 1

**Input**

```python
solve(4, 6, 2)
```

**Output**

```text
20
```

**Explanation.** Implement the lora parameter count operation.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
20
```

### Hint

r*in_features+r*out_features

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is LoRA Parameter Count?

Implement the lora parameter count operation. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

LoRA Parameter Count supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **r*in_features+r*out_features**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `r * (in_features + out_features)`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `(4,6,2)` returns `20`. Reversing its observation rows returns `20`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses Python arithmetic/iteration. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `r * (in_features + out_features)` after preparing the intermediates for LoRA Parameter Count. Python arithmetic/iteration directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
