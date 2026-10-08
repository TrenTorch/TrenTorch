---
name: research-clip-symmetric-loss
title: 'CLIP: The Symmetric Contrastive Loss'
tags: [research-papers, computer-vision, vision-language, contrastive]
difficulty: Advanced
---

## Statement

### The problem, from first principles

CLIP's loss treats each pair in both directions: for each image, pick its caption among the batch, and for each caption, pick its image. Averaging the two cross-entropies makes the objective symmetric.

### From theory to code

Implement `clip_symmetric_loss(logits)`, the mean of the row and column cross-entropies with diagonal targets.

### Constraints

- Use `logsumexp` for stability.

### Hints

<details>
<summary>Hint 1</summary>

For each direction, the loss per row is `logsumexp(row) - diagonal entry`. Average over rows for both the matrix and its transpose, then average the two.

</details>

## Theory

### The simple version

A uniform matrix gives log N, the chance level for N candidates. Each correct pair must beat every other candidate in its row and column.

### The formula

$$\mathcal{L} = \frac{1}{2}\left(\mathcal{L}_{i\to t} + \mathcal{L}_{t\to i}\right)$$

### How NumPy/PyTorch actually implements this

CLIP training calls `cross_entropy` on the logits and on their transpose with `arange(N)` targets, then averages.

## Explanation

Transposing the matrix swaps the roles of images and captions, so one cross-entropy function serves both directions.
