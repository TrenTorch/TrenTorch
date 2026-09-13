---
name: systems-perf-parameter-counting
title: Parameter Counting
tags: [mlops, profiling]
difficulty: Beginner
---

## Statement

### The problem, from first principles

"How big is this model?" is the very first question anyone asks about a network before they even train it — does it fit in memory, is it comparable to a known baseline, how much would fine-tuning it cost. The answer is a single number: the total count of individual learnable scalar values across every weight and bias tensor.

### From theory to code

Implement `count_parameters(params)`, the total element count across a list of parameter arrays, and `count_trainable_parameters(params, requires_grad)`, the same count restricted to parameters that are actually trainable (not frozen).

### Constraints

- `params`: a list of NumPy arrays of any shapes.
- `count_parameters` returns the sum of every array's total element count.
- `requires_grad`: a list of booleans, one per entry in `params`.
- `count_trainable_parameters` returns the sum of element counts only where the matching `requires_grad` entry is `True`.
- An empty `params` list returns `0`.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

A NumPy array's `.size` attribute is exactly its total element count, regardless of how many dimensions it has.

</details>

<details>
<summary>Hint 2</summary>

`count_trainable_parameters` is `count_parameters`'s same sum, but only over the `(param, trainable)` pairs where `trainable` is `True` — `zip(params, requires_grad)` pairs them up.

</details>

## Theory

### The simple version

Every weight matrix and bias vector in a network is a fixed-size grid of individually-adjustable numbers. Counting "how big" a model is means counting every single one of those numbers across every tensor the model owns — a `(4, 10)` weight matrix contributes `40` adjustable numbers, a `(4,)` bias contributes `4` more, and the model's total parameter count is just the sum across every tensor it has.

### The formula

```text
count_parameters(params) = sum(p.size for p in params)
count_trainable_parameters(params, requires_grad) = sum(p.size for p, rg in zip(params, requires_grad) if rg)
```

### How PyTorch actually implements this

`sum(p.numel() for p in model.parameters())` is the standard way to get this number for a real PyTorch model — `numel()` is exactly `.size`'s PyTorch equivalent. Restricting to trainable parameters is `sum(p.numel() for p in model.parameters() if p.requires_grad)`, since `requires_grad=False` (used for frozen layers, e.g. in transfer learning or parameter-efficient fine-tuning like `LoRA`) is exactly what a parameter's `requires_grad` attribute tracks in real PyTorch. Verified in this exercise's own `tests.py`, whose `test_11_matches_real_pytorch_module_parameter_counts` checks against real, offline-computed `torch.nn.Linear` and `torch.nn.Conv2d` parameter counts.

## Explanation

`count_parameters` sums `p.size` (NumPy's total-element-count attribute, working identically regardless of an array's number of dimensions) across every array in `params` — a `(4, 10)` weight array contributes `40`, a `(4,)` bias array contributes `4`, matching exactly how a real model's parameter count is computed tensor by tensor.

`count_trainable_parameters` performs the identical sum, but `zip(params, requires_grad)` pairs each array with its own trainability flag, and the `if trainable` filter skips any array whose flag is `False` — frozen parameters (common when only fine-tuning part of a pretrained model) still exist and take up memory, but don't count toward what's actually being learned.
