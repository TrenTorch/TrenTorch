---
name: research-byol-symmetric-loss
title: 'BYOL: The Symmetrized Loss'
tags: [research-papers, unsupervised, self-supervised, bootstrap]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

BYOL uses each view as a prediction target for the other one, and sums the two losses. This symmetry makes the objective treat both augmented views equally.

### From theory to code

Implement `symmetric_byol_loss(p1, z2, p2, z1)`, the sum of the two directional BYOL losses.

### Constraints

- The two directions use the target projection of the opposite view.

### Hints

<details>
<summary>Hint 1</summary>

Apply the single-direction loss to `(p1, z2)` and to `(p2, z1)`, then add.

</details>

## Theory

### The simple version

Summing both directions doubles the training signal per image pair and removes any preference for one view. The final loss is what the paper minimizes.

### The formula

$$\mathcal{L} = \tilde{\mathcal{L}}(p_1, z_2) + \tilde{\mathcal{L}}(p_2, z_1)$$

### How NumPy/PyTorch actually implements this

The loss is computed on the two views of each batch element and averaged over the batch.

## Explanation

The symmetrized loss is the standard choice in BYOL-style self-supervised methods.
