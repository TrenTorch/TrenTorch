---
name: research-simclr-l2-normalize
title: 'SimCLR: L2 Normalization of Projections'
tags: [research-papers, unsupervised, contrastive, self-supervised]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Before the contrastive loss, SimCLR's projection head output is normalized to unit length. That turns the dot product into a cosine similarity, so the loss depends only on direction.

### From theory to code

Implement `l2_normalize(z)`, returning the vector scaled to unit length.

### Constraints

- A zero vector is returned unchanged.

### Hints

<details>
<summary>Hint 1</summary>

Divide by the norm, guarding the zero case.

</details>

## Theory

### The simple version

Normalizing keeps every representation on the unit sphere, where cosine similarity is a simple dot product and no feature can dominate by magnitude.

### The formula

$$\hat z = \frac{z}{\lVert z\rVert_2}$$

### How NumPy/PyTorch actually implements this

`torch.nn.functional.normalize(z, dim=-1)` performs this step on batches.

## Explanation

On the unit sphere the cosine similarity and the Euclidean distance are monotonically related, which makes the two views of the loss equivalent.
