---
name: dl-core-reduction-ops
title: 'Reduction ops (sum, mean, max)'
tags: [deep-learning, tensors]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Most useful quantities aren't single numbers scattered across a tensor's dimensions — they're summaries: the total across a batch, the average score, the single best prediction. Reduction operations collapse many elements down to fewer, and getting the collapsed shape right (and, for `max`, getting more than just the value back) is where a lot of otherwise-correct-looking code quietly breaks downstream.

### From theory to code

Implement `sum_`, `mean_`, and `max_`, all taking `axis` and `keepdims`. `max_` is the odd one out: with `axis=None` it returns a single scalar like `np.max`, but with `axis` given, it must return `(values, indices)` — a real, distinctive difference from plain `np.max`.

### Constraints

- `a`: any NumPy array. `axis`: `None` (reduce over everything) or an integer axis.
- `keepdims`: when `True`, the reduced axis stays in the shape as size `1` instead of being removed.
- `sum_`/`mean_` return a plain array (or scalar when `axis=None`).
- `max_` with `axis=None` returns a plain scalar. With `axis` given, it returns a 2-tuple `(values, indices)`.
- None of the three mutate `a`.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`sum_` and `mean_` need nothing beyond passing `axis`/`keepdims` straight through to NumPy's own equivalents.

</details>

<details>
<summary>Hint 2</summary>

`max_` needs a real `if`: `axis is None` behaves like plain `np.max`, but any other `axis` needs both `np.max` AND `np.argmax` called with that same `axis`/`keepdims`, returned together.

</details>

## Theory

### The simple version

A reduction op collapses many elements down to fewer — `01-hypothesis-function`'s Theory already warned that collapsing a dimension is exactly where shape bugs hide: sum/mean over an axis removes it entirely by default, but `keepdims=True` leaves a size-`1` placeholder there instead, which is frequently what's actually wanted — a reduced result that still broadcasts cleanly against the original array without needing a separate reshape.

### The formula

`max` specifically carries more information than `sum`/`mean` do: the *value* of the maximum along an axis is only half the story, real code usually also needs to know *where* that maximum occurred (which class had the highest score, which position in a sequence). `torch.max(a, dim=...)` returns both pieces together for exactly this reason — `np.max` alone only ever answers the value half of that question.

### How PyTorch actually implements this

Context only, untested by your submission: `torch.sum`/`torch.mean` behave exactly like their NumPy counterparts here, and `torch.max(a, dim=...)` returns a `(values, indices)` named tuple when a dimension is given — the same two-piece return this exercise's `max_` reproduces by hand — while `torch.max(a)` with no dimension returns a plain scalar tensor.

## Explanation

`sum_`/`mean_` pass `axis`/`keepdims` straight through to `np.sum`/`np.mean`, which already implement the same reduction and shape-collapsing behavior `torch.sum`/`torch.mean` do: with `axis=None`, reduce over every element to a scalar; with a specific `axis`, reduce along just that dimension; `keepdims=True` leaves a size-`1` dimension where the reduced axis used to be instead of removing it entirely (useful for broadcasting the reduced result back against the original array).

`max_` is the one with a genuine gotcha: `np.max` only ever returns the maximum *values*. `torch.max(a, dim=...)`, when given a dimension, returns *both* the values and their indices along that dimension, `(values, indices)`, because knowing *which* element was the maximum is frequently just as useful as knowing its value (this is exactly the operation behind `argmax`-based classification, picking the predicted class). `max_` reproduces this by calling both `np.max` and `np.argmax` with the same `axis`/`keepdims` and returning them together, but only when `axis` is actually given — with `axis=None` there's no dimension for indices to be "along," so it returns a plain scalar, matching `torch.max(a)`'s own single-scalar behavior with no `dim` argument.
