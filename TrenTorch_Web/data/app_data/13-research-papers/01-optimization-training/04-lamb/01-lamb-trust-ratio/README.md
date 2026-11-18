---
name: research-lamb-trust-ratio
title: 'LAMB: The Trust Ratio'
tags: [research-papers, optimization, large-batch]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

LAMB (You et al., 2019) combines Adam's per-parameter scaling with a LARS-style layer trust ratio. The ratio compares the weight norm to the norm of the Adam direction, so each layer's step is sized relative to its weights.

### From theory to code

Implement `lamb_trust_ratio(w, r)`, the ratio of the weight norm to the update norm.

### Constraints

- Return a Python float.

### Hints

<details>
<summary>Hint 1</summary>

Divide the norm of the weights by the norm of the update direction.

</details>

## Theory

### The simple version

Using Adam's direction inside LARS's trust ratio is what lets LAMB train with very large batches without the per-layer scale problem.

### The formula

$$\phi_\ell = \frac{\lVert w_\ell\rVert}{\lVert r_\ell\rVert}$$

### How NumPy/PyTorch actually implements this

BERT pretraining in the paper uses this ratio per layer.

## Explanation

The hand case divides 5 by a unit-norm direction, giving 5.
