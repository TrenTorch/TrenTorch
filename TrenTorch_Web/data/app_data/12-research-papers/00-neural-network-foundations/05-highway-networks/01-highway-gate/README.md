---
name: research-highway-gate
title: 'Highway Networks: The Transform Gate'
tags: [research-papers, architecture, highway]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Very deep plain networks are hard to train because gradients vanish through many nonlinear layers. Highway networks (Srivastava, Greff & Schmidhuber, 2015) let each layer learn how much of its input to carry forward unchanged, using a learned gate.

### From theory to code

Implement `highway_gate(x, W, b)`, which returns the transform gate `t = sigmoid(x W^T + b)` for each feature.

### Constraints

- Gate values are in `(0, 1)`.
- `W` is square with shape `(D, D)`.

### Hints

<details>
<summary>Hint 1</summary>

Compute `z = x @ W.T + b` and apply the logistic function element-wise.

</details>

## Theory

### The simple version

A gate near 1 passes the transformed signal; a gate near 0 carries the input through unchanged. The network learns the gate per feature.

### The formula

$$t = \sigma(W_T x + b_T), \qquad \sigma(z) = \frac{1}{1 + e^{-z}}$$

### How NumPy/PyTorch actually implements this

`torch.sigmoid(x @ W.t() + b)` produces the same gate; `torch.nn.functional.linear` is the affine part.

## Explanation

The sigmoid is the standard logistic function, written with `np.exp`. The gate's bias controls the default behaviour: a negative bias starts the layer close to identity.
