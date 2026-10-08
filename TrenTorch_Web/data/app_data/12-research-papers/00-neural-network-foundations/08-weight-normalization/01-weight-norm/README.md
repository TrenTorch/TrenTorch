---
name: research-weight-norm
title: 'Weight Normalization: Reparameterizing the Weights'
tags: [research-papers, normalization, weight-norm]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Weight normalization (Salimans & Kingma, 2016) splits each weight vector into a length `g` and a direction `v / ||v||`. Training then adjusts length and direction separately, which speeds up optimization.

### From theory to code

Implement `weight_norm(v, g)`, which builds the weight matrix with each row of length `g[i]` pointing along `v[i]`.

### Constraints

- `v` has shape `(out, in)`, `g` has shape `(out,)`.

### Hints

<details>
<summary>Hint 1</summary>

Divide each row of `v` by its norm, then multiply each row by its `g` value.

</details>

## Theory

### The simple version

Separating magnitude from direction means the scale of a unit's weights is a single parameter, not a product of many weights. That decoupling is the reason the method helps optimization.

### The formula

$$\mathbf{w}_i = \frac{g_i}{\|\mathbf{v}_i\|}\,\mathbf{v}_i$$

### How NumPy/PyTorch actually implements this

`torch.nn.utils.parametrizations.weight_norm` applies the same reparameterization to a layer's weight.

## Explanation

`g[:, None]` broadcasts each scale across its row. Row norms are taken over the input dimension, matching how a linear layer uses its weights.
