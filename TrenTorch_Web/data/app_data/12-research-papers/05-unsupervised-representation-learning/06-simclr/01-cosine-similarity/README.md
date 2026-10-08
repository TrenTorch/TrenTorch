---
name: research-simclr-cosine
title: 'SimCLR: Cosine Similarity'
tags: [research-papers, unsupervised, contrastive, self-supervised]
difficulty: Beginner
---

## Statement

### The problem, from first principles

SimCLR (Chen et al., 2020) learns image features by making two augmented views of the same image agree. Agreement is measured by cosine similarity, which ignores the length of the vectors and only compares their direction.

### From theory to code

Implement `cosine_similarity(a, b)`, returning the cosine of the angle between two vectors.

### Constraints

- Return 0.0 for a zero vector instead of dividing by zero.

### Hints

<details>
<summary>Hint 1</summary>

Compute the dot product, divide by the product of the two norms.

</details>

## Theory

### The simple version

Normalizing by length means the contrastive loss depends only on direction, so the network cannot cheat by inflating the scale of its features.

### The formula

$$\text{sim}(a, b) = \frac{a^\top b}{\lVert a\rVert\,\lVert b\rVert}$$

### How NumPy/PyTorch actually implements this

`torch.nn.functional.cosine_similarity` computes the same value with a small epsilon for stability.

## Explanation

Cosine similarity is the dot product of the unit-normalized vectors, which SimCLR computes after its projection head.
