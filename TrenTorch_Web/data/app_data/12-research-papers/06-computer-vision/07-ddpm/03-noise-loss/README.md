---
name: research-ddpm-noise-loss
title: 'DDPM: The Noise Prediction Loss'
tags: [research-papers, computer-vision, diffusion, generative-models]
difficulty: Beginner
---

## Statement

### The problem, from first principles

DDPM's training objective is simple: predict the noise that was added to a sample. The network sees the noisy sample and the noise level, and is trained with mean squared error on the noise.

### From theory to code

Implement `noise_prediction_loss(eps, eps_pred)`, the mean squared error on the noise.

### Constraints

- Returns a Python float.

### Hints

<details>
<summary>Hint 1</summary>

Square the difference between the true and predicted noise, then average.

</details>

## Theory

### The simple version

Predicting the noise is equivalent to a weighted score-matching objective, and the simple unweighted form worked best in the paper's experiments.

### The formula

$$L_{\text{simple}} = \mathbb{E}_{x_0,\epsilon,t}\big[\lVert\epsilon - \epsilon_\theta(x_t, t)\rVert^2\big]$$

### How NumPy/PyTorch actually implements this

DDPM training loops compute `F.mse_loss(eps_pred, noise)` on each batch.

## Explanation

The loss is a plain regression, which is why diffusion models train stably with standard optimizers.
