---
name: research-ldm-cfg-combine
title: 'Latent Diffusion: Classifier-free Guidance'
tags: [research-papers, computer-vision, diffusion, latent]
difficulty: Advanced
---

## Statement

### The problem, from first principles

Classifier-free guidance sharpens how well samples match the text prompt. The model is run twice, once with and once without the condition, and the difference is amplified by a guidance weight.

### From theory to code

Implement `cfg_combine(eps_u, eps_c, w)`, returning the unconditional prediction pushed toward the conditional one by weight `w`.

### Constraints

- `w` can exceed one for stronger guidance.

### Hints

<details>
<summary>Hint 1</summary>

Compute the difference `eps_c - eps_u`, scale it by `w`, and add to `eps_u`.

</details>

## Theory

### The simple version

Larger w moves the prediction further toward the text-conditioned direction. Too large a value reduces diversity and can oversaturate images, so the weight is tuned.

### The formula

$$\tilde\epsilon = \epsilon_\theta(x_t) + w\,\big(\epsilon_\theta(x_t, c) - \epsilon_\theta(x_t)\big)$$

### How NumPy/PyTorch actually implements this

Stable Diffusion samplers run the U-Net on a batch of two (unconditional and conditional) and combine the outputs with this formula.

## Explanation

The combination is an extrapolation along the direction that the condition adds to the noise prediction.
