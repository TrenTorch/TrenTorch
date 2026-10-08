---
name: research-deep-forest-cascade-augment
title: 'Deep Forest: Augmenting Features With Class Vectors'
tags: [research-papers, classical-ml, ensembles, deep-forest]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Each Deep Forest layer receives the raw features together with the class vectors from the layer before, so the next forests can use the earlier layer's opinions as extra inputs.

### From theory to code

Implement `cascade_augment(X, class_vectors)`, which places the class vectors next to the original features.

### Constraints

- Both inputs have the same number of rows.

### Hints

<details>
<summary>Hint 1</summary>

Use `np.hstack` to join the two arrays column-wise.

</details>

## Theory

### The simple version

The augmented features give later layers the original input and a summary of what earlier layers already concluded, which is how the cascade refines its predictions.

### The formula

$$\tilde X_\ell = [\,X \;\|\; P_{\ell-1}\,]$$

### How NumPy/PyTorch actually implements this

Feature stacking with `np.hstack` or `torch.cat(dim=1)` is the standard way to build such cascaded inputs.

## Explanation

The concatenation is a column stack. Each layer's input width grows by the number of classes.
