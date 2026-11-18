---
name: research-mixup-loss
title: 'Mixup: The Mixed Loss'
tags: [research-papers, augmentation, mixup]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Because the target is a mix of two labels, the loss is also a mix. The paper's key observation is that the mixed loss equals the loss against the mixed target for cross-entropy, so the two views agree.

### From theory to code

Implement `mixup_loss(loss_a, loss_b, lam)`, returning `lam * loss_a + (1 - lam) * loss_b`.

### Constraints

- Works on scalars and arrays.

### Hints

<details>
<summary>Hint 1</summary>

It is a single weighted sum of the two loss values.

</details>

## Theory

### The simple version

Each label contributes to the loss in proportion to its mixing weight. Doing this per label is equivalent to using the mixed target directly.

### The formula

$$\mathcal{L} = \lambda\,\ell(f(\tilde x), y_a) + (1 - \lambda)\,\ell(f(\tilde x), y_b)$$

### How NumPy/PyTorch actually implements this

Training scripts compute this as `lam * criterion(out, ya) + (1 - lam) * criterion(out, yb)`.

## Explanation

With cross-entropy the two forms coincide because the loss is linear in the target. This makes mixup cheap: no extra forward passes are needed.
