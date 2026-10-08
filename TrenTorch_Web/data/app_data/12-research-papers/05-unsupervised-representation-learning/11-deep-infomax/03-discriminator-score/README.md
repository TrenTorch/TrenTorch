---
name: research-dim-discriminator-score
title: 'Deep InfoMax: The Bilinear Discriminator'
tags: [research-papers, unsupervised, mutual-information, representation]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Deep InfoMax scores pairs of local and global features with a learned bilinear discriminator. The score is high when the local feature is consistent with the global summary, which is what the mutual information estimate rewards.

### From theory to code

Implement `discriminator_score(local, global_vec, W)`, returning `local^T W global`.

### Constraints

- `W` has shape `(d_l, d_g)`.

### Hints

<details>
<summary>Hint 1</summary>

Multiply the local vector by the matrix, then dot with the global vector.

</details>

## Theory

### The simple version

The learned matrix maps local features into the space of global summaries, so the discriminator can decide whether a pair belongs together.

### The formula

$$T(x, y) = E(x)^\top W\, C(\tilde x)$$

### How NumPy/PyTorch actually implements this

Deep InfoMax implementations compute this for every local-global pair in a batch with one matrix product.

## Explanation

The score is the same bilinear form used in CPC, applied between a patch encoding and an image-level summary.
