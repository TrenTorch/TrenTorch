---
name: research-ntk-arc-cosine
title: 'Neural Tangent Kernel: The ReLU Arc-Cosine Kernel'
tags: [research-papers, classical-ml, kernels, ntk]
difficulty: Advanced
---

## Statement

### The problem, from first principles

For a wide ReLU network, the NTK between two inputs reduces to an arc-cosine kernel: a formula that depends only on the two input norms and the angle between them. Similar inputs score high and dissimilar ones score low, without any training.

### From theory to code

Implement `arc_cosine_kernel(x, y)`, using the norms of x and y and the angle between them.

### Constraints

- Return `0.0` when either vector is zero.

### Hints

<details>
<summary>Hint 1</summary>

Compute the angle `theta` from the normalized dot product, then apply `|x||y| / (2 pi) * (sin theta + (pi - theta) cos theta)`.

</details>

## Theory

### The simple version

The angle controls how much the kernel decays as inputs point in different directions. At angle zero it reduces to half the squared norm.

### The formula

$$k(x, y) = \frac{\lVert x\rVert\lVert y\rVert}{2\pi}\left(\sin\theta + (\pi - \theta)\cos\theta\right), \qquad \cos\theta = \frac{x \cdot y}{\lVert x\rVert\lVert y\rVert}$$

### How NumPy/PyTorch actually implements this

Kernel libraries implement the same expression for infinite-width ReLU networks, using `arccos` on the normalized inner product.

## Explanation

This is the closed form for the ReLU kernel of Cho & Saul (2009), which the NTK paper uses for fully-connected ReLU networks.
