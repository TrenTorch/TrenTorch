---
name: research-lamb-update
title: 'LAMB: The Layer-wise Update'
tags: [research-papers, optimization, large-batch]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

The LAMB step is the Adam direction, multiplied by the layer's trust ratio and the learning rate. Each layer moves a fixed fraction of its own weight norm per step.

### From theory to code

Implement `lamb_update(w, r, lr)`, one LAMB step for a single layer.

### Constraints

- Reuse the trust ratio definition from the previous question.

### Hints

<details>
<summary>Hint 1</summary>

Multiply the direction by lr and by the trust ratio, then subtract from the weights.

</details>

## Theory

### The simple version

Because the step length is lr times the weight norm, the update size is interpretable regardless of the scale of the gradient.

### The formula

$$w \leftarrow w - \eta\,\phi_\ell\,r_\ell$$

### How NumPy/PyTorch actually implements this

The step-length test confirms the norm of the change equals lr times the weight norm.

## Explanation

Hand case: the ratio is 5, so the step is 0.5 times [0.6, 0.8], giving [2.7, 3.6].
