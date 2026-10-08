---
name: research-aae-recon-mse
title: 'Adversarial Autoencoders: The Reconstruction Loss'
tags: [research-papers, unsupervised, autoencoders, adversarial]
difficulty: Beginner
---

## Statement

### The problem, from first principles

An adversarial autoencoder (Makhzani et al., 2015) is an autoencoder whose latent codes are also pushed toward a chosen prior by a discriminator. The first part is an ordinary reconstruction loss, mean squared error here.

### From theory to code

Implement `reconstruction_mse(x, x_hat)`, the mean squared error over all entries.

### Constraints

- Average over every element.

### Hints

<details>
<summary>Hint 1</summary>

Square the differences, then take the mean.

</details>

## Theory

### The simple version

Reconstruction keeps the code faithful to the input. The adversarial term, covered in the next question, shapes the code distribution.

### The formula

$$\mathcal{L}_{\text{rec}} = \frac{1}{n}\sum_i \lVert x_i - \hat x_i\rVert^2$$

### How NumPy/PyTorch actually implements this

Autoencoder implementations compute this with `F.mse_loss(x_hat, x)`.

## Explanation

The loss is the usual autoencoder objective; the paper keeps it and adds a discriminator on the latent space.
