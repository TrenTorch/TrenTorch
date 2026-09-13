---
name: systems-perf-magnitude-pruning
title: Magnitude-Based Pruning, Single Step
tags: [mlops, neural-networks, compression]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Quantization (`02-quantization`) shrinks a model by storing each weight with fewer bits. Pruning takes a different approach: instead of representing every weight more cheaply, remove some weights entirely by setting them to exactly zero — a matrix with many exact zeros compresses well and, with the right hardware/software support, skips computation on those zeros altogether.

### From theory to code

Implement `magnitude_prune(weight, sparsity)`, which zeros out the smallest-magnitude fraction of a weight array's elements, leaving the rest untouched. The underlying premise: a weight already close to zero contributes almost nothing to the layer's output, so removing the smallest ones should hurt accuracy far less than removing an equally-sized random selection would.

### Constraints

- `weight`: any-shape float array. `sparsity`: a fraction in `[0, 1]`, the proportion of elements to zero out.
- Elements are ranked by absolute value; the `sparsity` fraction with the _smallest_ magnitude get zeroed.
- `sparsity <= 0` prunes nothing (returns an unchanged copy).
- Returns a new array — never modifies `weight` in place.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`np.partition(flat_abs, k-1)[k-1]` finds the value that would sit at position `k-1` in a full sort, without actually sorting the whole array — exactly the threshold value at "the smallest `k` elements' boundary."

</details>

<details>
<summary>Hint 2</summary>

Once you have that threshold, a boolean mask `np.abs(weight) > threshold` is `True` for every element that survives pruning — multiplying `weight` by that mask zeros out everything else in one step.

</details>

## Theory

### The simple version

Imagine a weight matrix as a crowd of contributors to a group decision, where each contributor's "voice" is proportional to the absolute value of their weight. Someone whose voice is already nearly inaudible (a weight near zero) isn't meaningfully changing the group's decision either way — removing them entirely (setting their weight to exactly `0`) should barely be noticeable, while removing an equally-sized _random_ selection of contributors (including some loud ones) would clearly change the outcome.

### The formula

```text
threshold = the value at position floor(sparsity * size) in a sorted-ascending list of |weight|
mask      = |weight| > threshold
pruned    = weight * mask
```

### How PyTorch actually implements this

`torch.nn.utils.prune.l1_unstructured(module, name="weight", amount=sparsity)` implements exactly this scheme — verified directly in this exercise's own `tests.py`, whose `test_10_matches_real_pytorch_l1_unstructured_pruning_on_a_baked_reference_case` bakes in a pruned weight matrix generated once, offline, from a real call to PyTorch's own pruning utility. Real pruning workflows rarely stop at one single-shot pass at a high sparsity target — `02-iterative-pruning-schedule` builds on this exact function to reach a high final sparsity gradually, which tends to preserve far more accuracy than pruning everything in one shot.

## Explanation

`magnitude_prune` flattens `|weight|` and uses `np.partition` to find the value at the boundary between "the `num_to_prune` smallest-magnitude elements" and everything else — `np.partition` is faster than a full `np.sort` here since it only needs one specific order statistic, not a complete ranking. The boolean mask `np.abs(weight) > threshold` is `True` wherever an element's magnitude exceeds that boundary (survives), `False` at or below it (gets pruned), and `weight * mask` applies that mask elementwise, producing exact zeros wherever the mask is `False` while leaving every surviving element completely unchanged.
