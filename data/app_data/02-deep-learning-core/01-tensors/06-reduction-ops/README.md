---
name: dl-core-reduction-ops
title: 'Reduction ops (sum, mean, max)'
tags: [deep-learning, tensors]
difficulty: Beginner
---

## Statement

Implement:

```python
def sum_(a, axis=None, keepdims=False) -> np.ndarray: ...
def mean_(a, axis=None, keepdims=False) -> np.ndarray: ...
def max_(a, axis=None, keepdims=False): ...
```

- `max_` with `axis=None` returns a single scalar, the same as `np.max`. With `axis` given, it returns `(values, indices)`, a real, distinctive difference from `np.max`.

## Theory

A reduction op collapses many elements down to fewer, `01-hypothesis-function`'s Theory already warned that collapsing a dimension is exactly where shape bugs hide: sum/mean over an axis removes it entirely by default, but `keepdims=True` leaves a size-`1` placeholder there instead, which is frequently what's actually wanted, a reduced result that still broadcasts cleanly against the original array without needing a separate reshape.

`max` specifically carries more information than `sum`/`mean` do: the _value_ of the maximum along an axis is only half the story, real code usually also needs to know _where_ that maximum occurred (which class had the highest score, which position in a sequence). `torch.max(a, dim=...)` returns both pieces together for exactly this reason, `np.max` alone only ever answers the value half of that question.

## Explanation

`sum_`/`mean_` pass `axis`/`keepdims` straight through to `np.sum`/`np.mean`, which already implement the same reduction and shape-collapsing behavior `torch.sum`/`torch.mean` do: with `axis=None`, reduce over every element to a scalar; with a specific `axis`, reduce along just that dimension; `keepdims=True` leaves a size-`1` dimension where the reduced axis used to be instead of removing it entirely (useful for broadcasting the reduced result back against the original array).

`max_` is the one with a genuine gotcha: `np.max` only ever returns the maximum _values_. `torch.max(a, dim=...)`, when given a dimension, returns _both_ the values and their indices along that dimension, `(values, indices)`, because knowing _which_ element was the maximum is frequently just as useful as knowing its value (this is exactly the operation behind `argmax`-based classification, picking the predicted class). `max_` reproduces this by calling both `np.max` and `np.argmax` with the same `axis`/`keepdims` and returning them together, but only when `axis` is actually given, with `axis=None` there's no dimension for indices to be "along," so it returns a plain scalar, matching `torch.max(a)`'s own single-scalar behavior with no `dim` argument.
