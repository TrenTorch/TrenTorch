---
name: research-gan-optimal-discriminator
title: 'GAN: The Optimal Discriminator'
tags: [research-papers, unsupervised, gan, generative-models]
difficulty: Advanced
---

## Statement

### The problem, from first principles

The GAN paper shows that for a fixed generator, the best discriminator outputs the ratio of the data density to the sum of the two densities. When the generator matches the data, this ratio is one half everywhere, the equilibrium of the game.

### From theory to code

Implement `optimal_discriminator(p_data, p_model)`, returning the density ratio element-wise.

### Constraints

- Densities are nonnegative and not both zero at any point.

### Hints

<details>
<summary>Hint 1</summary>

Divide `p_data` by `p_data + p_model`.

</details>

## Theory

### The simple version

The discriminator should be confident where data is more likely than generated samples. When the two densities match, no discriminator can do better than chance.

### The formula

$$D^*(x) = \frac{p_{\text{data}}(x)}{p_{\text{data}}(x) + p_g(x)}$$

### How NumPy/PyTorch actually implements this

The formula explains why GAN training stalls when the discriminator is too strong or too weak.

## Explanation

Substituting this optimum into the discriminator loss gives a Jensen-Shannon divergence between the data and generator distributions, which the paper uses to explain the game.
