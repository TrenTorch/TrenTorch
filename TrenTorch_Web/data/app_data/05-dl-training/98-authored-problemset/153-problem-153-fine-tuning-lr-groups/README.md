---
name: problem-153-fine-tuning-lr-groups
title: Fine-Tuning LR Groups
tags: [dl-training-theory, case-study, hard, fine-tuning., company-case]
difficulty: Advanced
---

## Statement

Implement `solve(backbone, head, base_lr, backbone_factor)`. Assign a smaller learning rate to a backbone than to a new head. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** Grab is scenario context only; this is not an official Grab interview question or endorsement.

### Example 1

**Input**

```python
solve(['b1', 'b2'], ['h1'], 0.01, 0.1)
```

**Output**

```text
[{'params': ['b1', 'b2'], 'lr': 0.001}, {'params': ['h1'], 'lr': 0.01}]
```

**Explanation.** Assign a smaller learning rate to a backbone than to a new head.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
[{'params': ['b2', 'b1'], 'lr': 0.0005625000000000001}, {'params': ['h1'], 'lr': 0.0075}]
```

### Hint

construct parameter groups

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Fine-Tuning LR Groups?

Assign a smaller learning rate to a backbone than to a new head. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Fine-Tuning LR Groups supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **construct parameter groups**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `[{'params': backbone, 'lr': base_lr * backbone_factor}, {'params': head, 'lr': base_lr}]`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `(['b1','b2'],['h1'],.01,.1)` returns `[{'params': ['b1', 'b2'], 'lr': 0.001}, {'params': ['h1'], 'lr': 0.01}]`. Reversing its observation rows returns `[{'params': ['b2', 'b1'], 'lr': 0.0005625000000000001}, {'params': ['h1'], 'lr': 0.0075}]`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses Python arithmetic/iteration. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `[{'params': backbone, 'lr': base_lr * backbone_factor}, {'params': head, 'lr': base_lr}]` after preparing the intermediates for Fine-Tuning LR Groups. Python arithmetic/iteration directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
