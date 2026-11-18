---
name: research-moco-momentum-update
title: 'MoCo: The Momentum Encoder Update'
tags: [research-papers, unsupervised, contrastive, momentum]
difficulty: Beginner
---

## Statement

### The problem, from first principles

MoCo (He et al., 2020) keeps a queue of negative keys produced by a slowly moving encoder. Using a momentum update rather than gradients keeps the keys consistent across the queue, which is what makes the queue usable.

### From theory to code

Implement `momentum_update(key, query, m)`, returning the momentum-weighted blend of the key and query parameters.

### Constraints

- `m` is close to 1, typically 0.999.

### Hints

<details>
<summary>Hint 1</summary>

Weight the key parameters by `m` and the query parameters by `1 - m`.

</details>

## Theory

### The simple version

A slowly changing key encoder means keys stored long ago are still roughly comparable with new queries, so a large queue of negatives remains valid.

### The formula

$$\theta_k \leftarrow m\,\theta_k + (1 - m)\,\theta_q$$

### How NumPy/PyTorch actually implements this

MoCo implementations apply this blend to every parameter after each query update.

## Explanation

The key encoder receives no gradients; it only follows the query encoder through this exponential average.
