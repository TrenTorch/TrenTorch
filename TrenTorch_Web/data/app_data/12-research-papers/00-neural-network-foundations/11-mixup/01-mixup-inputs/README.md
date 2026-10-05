---
name: research-mixup-inputs
title: 'Mixup: Blending Two Training Examples'
tags: [research-papers, augmentation, mixup]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Mixup (Zhang et al., 2018) trains on convex combinations of pairs of examples and their labels. It is a simple augmentation that smooths the decision boundary between classes.

### From theory to code

Implement `mixup_inputs(x, perm, lam)`, which blends each example with the example at its permuted index using weight `lam`.

### Constraints

- `lam` is in `[0, 1]`.
- `perm` is a permutation of the batch indices.

### Hints

<details>
<summary>Hint 1</summary>

Index the batch with `perm` to get the partners, then take the weighted sum.

</details>

## Theory

### The simple version

A mixed example sits between two training points, so the model sees intermediate inputs that encourage linear behaviour between classes.

### The formula

$$\tilde x = \lambda\, x_i + (1 - \lambda)\, x_{\pi(i)}$$

### How NumPy/PyTorch actually implements this

Frameworks implement this with `x[perm]` and a scalar weight, the same two lines as here.

## Explanation

Indexing with `perm` creates the random pairing. The same `lam` is used across the batch in the paper's setup.
