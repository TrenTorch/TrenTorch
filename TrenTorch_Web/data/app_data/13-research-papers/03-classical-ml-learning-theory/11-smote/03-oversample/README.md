---
name: research-smote-oversample
title: 'SMOTE: Oversampling a Minority Class'
tags: [research-papers, classical-ml, imbalance, smote]
difficulty: Advanced
---

## Statement

### The problem, from first principles

The full SMOTE step repeats three things: pick a minority sample, pick one of its nearest minority neighbors, and create a point between them. Repeating this builds up the minority class without copying existing rows.

### From theory to code

Implement `smote_oversample(X, n_new, k, rng)`, which creates `n_new` synthetic minority samples by interpolating random neighbor pairs.

### Constraints

- Partners come from the `k` nearest neighbors, excluding the sample itself.

### Hints

<details>
<summary>Hint 1</summary>

Draw a sample index, sort its distances to find neighbors (skipping the first, which is itself), draw a neighbor, draw `u`, then interpolate.

</details>

## Theory

### The simple version

Because every synthetic point lies on a segment between two minority samples, the new data stays in the region the minority class already occupies.

### The formula

$$x_{\text{new}} = x_i + u\,(x_j - x_i), \qquad x_j \in \mathcal{N}_k(x_i),\; u \sim \text{Uniform}(0,1)$$

### How NumPy/PyTorch actually implements this

`imblearn.over_sampling.SMOTE` implements this loop over the whole minority class.

## Explanation

The algorithm is the random composition of the two previous steps. Using the provided `rng` makes the oversampling reproducible.
