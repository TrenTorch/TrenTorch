---
name: research-he-init-sample
title: 'He Initialization: Sampling a Weight Matrix'
tags: [research-papers, initialization, relu]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

A weight matrix sampled naively, with the same scale for every layer, makes activations explode or vanish with depth. The initialization must match the layer's width and activation function.

### From theory to code

Implement `he_init_weights(fan_in, fan_out, rng)`, which returns a `(fan_out, fan_in)` matrix sampled with He's standard deviation.

### Constraints

- `rng` is a `numpy.random.Generator`.
- The result has shape `(fan_out, fan_in)`.

### Hints

<details>
<summary>Hint 1</summary>

Use `rng.normal(0, std, size=...)` with `std = sqrt(2 / fan_in)`.

</details>

## Theory

### The simple version

This is the sampling step that `he_init_std` describes. Using the fan-in rather than the fan-out keeps forward-pass activations at a stable scale.

### The formula

$$W_{ij} \sim \mathcal{N}\left(0, \frac{2}{n_{\text{in}}}\right)$$

### How NumPy/PyTorch actually implements this

`torch.nn.init.kaiming_normal_` draws from the same distribution in place on a parameter tensor.

## Explanation

Each entry is drawn independently. The shape is `(fan_out, fan_in)` so that `x @ W.T` maps `fan_in` inputs to `fan_out` outputs.
