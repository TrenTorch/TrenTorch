---
name: research-vq-loss
title: 'VQ-VAE: The Vector-quantization Loss'
tags: [research-papers, unsupervised, discrete-latents, vae]
difficulty: Advanced
---

## Statement

### The problem, from first principles

The VQ-VAE loss has three parts: reconstruction, a codebook term that moves codes toward encoder outputs, and a commitment term that keeps encoder outputs near their codes. The two quantization terms share a squared-distance form.

### From theory to code

Implement `vq_loss(z, e, beta)`, returning the mean squared distance scaled by `(1 + beta)`.

### Constraints

- Forward values follow the paper's two quantization terms.

### Hints

<details>
<summary>Hint 1</summary>

Compute the mean squared difference between encoder outputs and codes, then weight it by `1 + beta`.

</details>

## Theory

### The simple version

The codebook term updates the codes and the commitment term updates the encoder. Both pull them together, so the discrete code stays a faithful summary of the encoder output.

### The formula

$$\mathcal{L}_{\text{VQ}} = \lVert \text{sg}[z_e] - e\rVert^2 + \beta\,\lVert z_e - \text{sg}[e]\rVert^2$$

### How NumPy/PyTorch actually implements this

VQ-VAE training code computes both terms with `detach` calls on the appropriate side.

## Explanation

The stop-gradient operator sg controls which side each term updates. Numerically both terms share the same forward value, which is what this question computes.
