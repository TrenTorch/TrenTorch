---
name: research-simclr-nt-xent
title: 'SimCLR: The NT-Xent Loss for One Anchor'
tags: [research-papers, unsupervised, contrastive, self-supervised]
difficulty: Advanced
---

## Statement

### The problem, from first principles

SimCLR's contrastive loss, NT-Xent, asks for each anchor to pick its positive out of all the other views in the batch. It is a softmax cross-entropy over cosine similarities scaled by a temperature.

### From theory to code

Implement `nt_xent_anchor(sim_pos, sims_neg, tau)`, the softmax loss of the positive among the candidates.

### Constraints

- Use `logaddexp` for numerical stability.

### Hints

<details>
<summary>Hint 1</summary>

Stack the positive and negative similarities divided by `tau`, then compute `logsumexp` minus the positive's logit.

</details>

## Theory

### The simple version

A low loss requires the anchor to be far more similar to its own view than to any other image in the batch. The temperature controls how sharply the softmax separates them.

### The formula

$$\ell_{i,j} = -\log\frac{\exp(\text{sim}(z_i, z_j)/\tau)}{\sum_{k \neq i}\exp(\text{sim}(z_i, z_k)/\tau)}$$

### How NumPy/PyTorch actually implements this

SimCLR implementations build the full similarity matrix and apply `cross_entropy` with the positive as the target class.

## Explanation

The sum runs over all other samples in the batch, so larger batches give harder negatives and better features.
