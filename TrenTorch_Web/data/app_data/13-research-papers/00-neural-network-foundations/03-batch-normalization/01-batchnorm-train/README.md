---
name: research-batchnorm-train
title: 'Batch Normalization: The Training-Time Forward Pass'
tags: [research-papers, normalization, batchnorm]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Activations drift in scale and offset as earlier layers change during training. Batch normalization (Ioffe & Szegedy, 2015) renormalizes each feature across the mini-batch, which stabilizes and speeds up training.

### From theory to code

Implement `batchnorm_train(x, gamma, beta, eps)`, which normalizes each feature with the batch mean and variance, then applies the learned scale and shift. Return the output along with the mean and variance it used.

### Constraints

- `x` has shape `(N, D)`.
- Use the biased (population) variance, dividing by `N`.

### Hints

<details>
<summary>Hint 1</summary>

Compute `mean` and `var` over axis 0, normalize with `sqrt(var + eps)`, then apply `gamma * x_hat + beta`.

</details>

## Theory

### The simple version

Each feature is shifted to zero mean and scaled to unit variance across the batch. `gamma` and `beta` then restore whatever scale and offset the layer needs, so normalization never removes representational power.

### The formula

$$\mu_B = \frac{1}{N}\sum_i x_i, \quad \sigma_B^2 = \frac{1}{N}\sum_i (x_i - \mu_B)^2, \quad y_i = \gamma \frac{x_i - \mu_B}{\sqrt{\sigma_B^2 + \epsilon}} + \beta$$

### How NumPy/PyTorch actually implements this

`torch.nn.BatchNorm1d` computes exactly this in training mode and tracks the running mean and variance for later inference.

## Explanation

This is the per-feature normalization over the batch axis. Keeping `mean` and `var` returned lets the caller update running statistics for inference.
