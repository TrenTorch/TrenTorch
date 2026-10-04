---
name: dl-training-instance-norm
title: Instance Normalization
tags: [deep-learning, training, normalization]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Instance Normalization normalizes each instance (sample) and channel independently, ignoring batch statistics. Unlike BatchNorm which pools across the batch, InstanceNorm computes mean/variance per instance-channel pair.

$$\text{instance\_norm}(x, \gamma, \beta, \epsilon) = \gamma \frac{x - \mu_{nc}}{\sqrt{\sigma_{nc}^2 + \epsilon}} + \beta$$

Where mu_nc and sigma_nc are computed per instance and channel (across spatial dimensions).

### From theory to code

Implement:

```python
instance_norm(x, gamma, beta, eps=1e-5)
```

### Constraints

- x shape: (N, C, H, W) or (N, C)
- gamma, beta shape (C,)
- Return normalized x, same shape.

## Theory

InstanceNorm is useful for style transfer and tasks where batch statistics are harmful. It removes instance-specific information while preserving channel-specific statistics.

## Explanation

For each instance and channel, compute mean/var across spatial dimensions, normalize, reshape back, scale/shift with gamma/beta.
