---
name: dl-training-group-norm
title: Group Normalization
tags: [deep-learning, training, normalization]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Group Normalization divides channels into groups and normalizes within each group. Unlike BatchNorm which normalizes across batch dimension, GroupNorm normalizes within spatial dimensions and groups.

$$\text{group\_norm}(x, \text{num\_groups}, \gamma, \beta, \epsilon) = \gamma \frac{x - \mu_g}{\sqrt{\sigma_g^2 + \epsilon}} + \beta$$

Where mu_g and sigma_g are computed per group (across spatial/channel within group).

### From theory to code

Implement:

```python
group_norm(x, num_groups, gamma, beta, eps=1e-5)
```

### Constraints

- x shape: (N, C, H, W) or (N, C)
- num_groups divides C.
- gamma, beta same shape as x[0] (channels).
- Return normalized x, same shape.

## Theory

GroupNorm is useful when batch size is small or variable, unlike BatchNorm which needs large batches.

## Explanation

Reshape to (N, num_groups, C/num_groups, -1), compute mean/var per group, normalize, reshape back, scale/shift.
