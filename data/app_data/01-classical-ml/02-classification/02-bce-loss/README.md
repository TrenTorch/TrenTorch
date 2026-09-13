---
name: classification-bce-loss
title: Binary Cross-Entropy Loss
tags: [classical-ml, classification, loss-functions]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Classification needs to distinguish uncertainty from confidently choosing the wrong class. A loss should therefore charge a much larger cost when a predicted probability disagrees with the true binary label. The logarithm does that, but only if its input is kept away from zero.

### From theory to code

Implement `bce_loss(p, y)` as a batch mean. Theory gives the two label cases; clip probabilities before either logarithm and return a Python `float`.

### Constraints

- `p` and binary `y` have matching `(n_samples,)` shapes.
- Clip `p` to `[1e-12, 1 - 1e-12]` before logs.
- Average one loss value per sample and return a plain `float`.
- Saturated `0.0` and `1.0` inputs must produce a finite loss.
- Use vectorized NumPy operations only.

### Hints

Open one at a time. Each gives away a little more than the last.

<details><summary>Hint 1</summary>

Each label selects one of two complementary probability terms.

</details>

<details><summary>Hint 2</summary>

Clip once, then form both `log(p)` and `log(1 - p)` before taking the negative mean.

</details>

## Theory

### The simple version

A correct confident prediction should be cheap; a wrong confident prediction should be expensive. Logarithms turn probability assigned to the truth into that asymmetric penalty.

### The formula

```text
p_safe = clip(p, 1e-12, 1 - 1e-12)
loss = -mean(y * log(p_safe) + (1 - y) * log(1 - p_safe))
```

For a positive label the first term remains; for a negative label the second remains.

### How PyTorch actually implements this

Context only, untested by your submission: `torch.nn.functional.binary_cross_entropy` computes binary cross-entropy from probabilities. This NumPy exercise defines its own pre-log clipping behavior.

## Explanation

The first line clips `p` at `1e-12` and `1 - 1e-12`, preventing either log argument from becoming zero. The return expression forms both vectorized label terms, reduces them with `np.mean`, negates the result, and wraps it in `float` so callers receive a Python scalar rather than a NumPy scalar.
