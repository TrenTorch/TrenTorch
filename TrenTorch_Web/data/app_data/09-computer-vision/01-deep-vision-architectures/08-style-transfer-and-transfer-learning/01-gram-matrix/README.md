---
name: vision-gram-matrix
title: Gram Matrix & Style
tags: [computer-vision, style-transfer, features, gram-matrix]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

What is the "style" of a painting, as opposed to its content? Gatys and colleagues made the idea precise with the feature maps of a pretrained CNN. A layer produces `C` feature maps over `H x W` positions. The **content** is _where_ features fire. The **style** is _which features fire together_, regardless of position, and that is exactly what the **Gram matrix** records: entry `(i, j)` is the inner product of feature map `i` with feature map `j`, summed over all positions. Swirly brushstrokes make certain channels co-activate everywhere, and the position information, which says where the swirls are, has been summed away.

### From theory to code

Implement `gram_matrix`.

### Constraints

- `features` has shape `(C, H, W)`. Flatten each channel to a vector of length `H * W`, giving `F` of shape `(C, H * W)`.
- Return `F @ F.T / (C * H * W)`, a symmetric `(C, C)` matrix. The normalization makes values comparable across layers of different sizes.

### Hints

<details>
<summary>Hint 1</summary>

`features.reshape(C, -1)` flattens the spatial dimensions.

</details>

<details>
<summary>Hint 2</summary>

Moving the same texture to a different position leaves the Gram matrix unchanged, which the tests check.

</details>

## Theory

### The simple version

Two paintings of different scenes can still be by the same artist: the same pairs of colours and strokes appear together. The Gram matrix is a table of "how often does stroke type i go with stroke type j".

### The formula

$$
G_{ij} = \frac{1}{CHW}\sum_{p=1}^{HW} F_{ip}F_{jp}, \qquad G = \frac{1}{CHW} F F^\top
$$

$G$ is positive semidefinite, and any permutation of the positions $p$ leaves it unchanged.

### How this is done in practice

Neural style transfer computes Gram matrices at several VGG layers for the style image and matches them with the generated image. The same statistic, in other forms, appears in texture synthesis, in adaptive instance normalization (channel means and variances) and in feature-covariance regularizers.

## Explanation

One reshape and one matrix product. The invariance tests are what make the matrix a _style_ descriptor: it is blind to where things are.
