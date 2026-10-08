---
name: research-cpc-bilinear-score
title: 'CPC: The Bilinear Compatibility Score'
tags: [research-papers, unsupervised, predictive-coding, contrastive]
difficulty: Beginner
---

## Statement

### The problem, from first principles

CPC scores each candidate future with a bilinear function of the context and the future latent. The matrix W is learned, and it lets the score depend on the relation between the two vectors, not only on their dot product.

### From theory to code

Implement `bilinear_score(c, W, z)`, returning `c^T W z`.

### Constraints

- `W` need not be square.

### Hints

<details>
<summary>Hint 1</summary>

Multiply the context by the matrix, then dot with the latent.

</details>

## Theory

### The simple version

A bilinear form is the simplest way to compare two vectors from different spaces. The learned matrix converts one into the other's coordinate system.

### The formula

$$s(c, z) = c^\top W z$$

### How NumPy/PyTorch actually implements this

The CPC code computes this as `torch.einsum('bd,de,be->b', c, W, z)`.

## Explanation

With W equal to the identity, the score reduces to a plain dot product, which the first test checks.
