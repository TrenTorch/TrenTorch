---
name: research-byol-loss
title: 'BYOL: The Normalized Regression Loss'
tags: [research-papers, unsupervised, self-supervised, bootstrap]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

BYOL (Grill et al., 2020) learns without negative pairs at all. An online network predicts the output of a slowly updated target network for another view of the same image. The loss is a normalized regression, which equals two minus twice the cosine similarity.

### From theory to code

Implement `byol_loss(p, z)`, returning `2 - 2 cos(p, z)`.

### Constraints

- Divide by both norms; no zero vectors.

### Hints

<details>
<summary>Hint 1</summary>

Compute the cosine similarity of the two vectors and apply `2 - 2 cos`.

</details>

## Theory

### The simple version

Minimizing the loss aligns the prediction with the target's direction. The target is a moving average of the online network, which keeps the problem from collapsing to a constant.

### The formula

$$\mathcal{L} = \left\lVert \frac{p}{\lVert p\rVert} - \frac{z}{\lVert z\rVert}\right\rVert^2 = 2 - 2\frac{p^\top z}{\lVert p\rVert\lVert z\rVert}$$

### How NumPy/PyTorch actually implements this

BYOL implementations compute the same cosine on normalized predictor and projector outputs.

## Explanation

The two forms are equal because squared distance between unit vectors is two minus twice their dot product.
