---
name: classification-production-bce-with-logits
title: 'Production Engineering: Fused, Numerically-Stable Loss'
tags: [classical-ml, classification, production-engineering, numerical-stability]
difficulty: Advanced
---

## Statement

### The problem, from first principles

Computing sigmoid first can round extreme logits to exact probabilities of zero or one before BCE sees them. A production loss avoids that irreversible step: it scores raw logits directly using an equivalent expression whose exponential never grows.

### From theory to code

Implement `bce_with_logits_loss(z, y)` without calling sigmoid. Theory gives the fused per-sample expression and explains why the exponent must receive a non-positive value.

### Constraints

- `z` and binary `y` have matching shapes.
- Return the mean loss as a Python `float`.
- Never create a sigmoid probability array or call `exp` on a positive value.
- Use `np.maximum(z, 0)`, `np.log1p`, and `np.exp(-np.abs(z))`.
- Remain finite for extreme positive and negative logits.

### Hints

Open one at a time. Each gives away a little more than the last.

<details><summary>Hint 1</summary>

Separate the expression into a piecewise-linear correction and a small logarithmic remainder.

</details>

<details><summary>Hint 2</summary>

`-np.abs(z)` is never positive; take its exponential, then use `log1p` for the logarithmic term.

</details>

## Theory

### The simple version

The fused loss keeps the useful information in a very confident score instead of first flattening it into a rounded probability. It rewrites the same penalty so the only exponential is safely at most one.

### The formula

```text
max_z_zero = maximum(z, 0)
stable_log_term = log1p(exp(-abs(z)))
per_sample = max_z_zero - z * y + stable_log_term
loss = mean(per_sample)
```

Because `-abs(z) <= 0`, `exp(-abs(z))` cannot overflow.

### How PyTorch actually implements this

Context only, untested by your submission: the test suite includes an offline-generated oracle from `torch.nn.functional.binary_cross_entropy_with_logits` for logits including `800` and `-800`. `torch.nn.BCEWithLogitsLoss` is the corresponding module API.

## Explanation

`max_z_zero = np.maximum(z, 0)` supplies the branch-dependent linear term without a Python branch. `stable_log_term = np.log1p(np.exp(-np.abs(z)))` both preserves precision for a tiny exponential and guarantees its exponent is non-positive. `per_sample` combines those exact formula terms, and `float(np.mean(per_sample))` reduces the batch without clipping a saturated probability.
