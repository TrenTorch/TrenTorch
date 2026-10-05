---
name: research-dropout-expectation
title: 'Dropout: Averaging Over Masks Recovers the Input'
tags: [research-papers, regularization, dropout]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Dropout is random, so a single forward pass is noisy. The paper's key claim is that the average over many dropout masks behaves like the un-dropped network with the right scaling. This question checks that claim numerically.

### From theory to code

Implement `dropout_expectation(x, p, n_samples, rng)` that draws `n_samples` masks, applies inverted dropout to each, and returns the mean.

### Constraints

- `rng` is a `numpy.random.Generator`.
- `n_samples` is a positive integer.

### Hints

<details>
<summary>Hint 1</summary>

Draw all masks at once with `rng.random((n_samples,) + x.shape) >= p`, then average over axis 0.

</details>

## Theory

### The simple version

Each kept unit is scaled by `1 / (1 - p)`, so its expected value is `(1 - p) * x / (1 - p) = x`. Averaging many masks estimates that expectation.

### The formula

$$\mathbb{E}_m\left[\frac{m \odot x}{1 - p}\right] = x, \qquad m_i \sim \text{Bernoulli}(1 - p)$$

### How NumPy/PyTorch actually implements this

`torch.distributions.Bernoulli` draws the masks, and averaging many dropout passes in `model.train()` mode approximates `model.eval()` output.

## Explanation

The function is a Monte Carlo estimate of this expectation. Increasing `n_samples` reduces the noise, which is the same reason ensemble averages approximate the paper's network-averaging view.
