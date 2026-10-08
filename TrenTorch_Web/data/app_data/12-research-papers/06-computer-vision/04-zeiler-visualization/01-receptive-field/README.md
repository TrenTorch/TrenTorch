---
name: research-zeiler-receptive-field
title: 'Visualizing Convolutional Networks: The Receptive Field'
tags: [research-papers, computer-vision, cnn, interpretability]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Zeiler and Fergus (2014) visualized which input pixels drive each unit. The receptive field, the region of the input a unit depends on, depends on every layer's kernel and on the strides before it.

### From theory to code

Implement `receptive_field(kernels, strides)`, returning the receptive field of the last layer's output.

### Constraints

- Strides multiply the spacing of later units.

### Hints

<details>
<summary>Hint 1</summary>

Start with a field of 1 and jump of 1. For each layer add `(k - 1) * jump`, then multiply the jump by the stride.

</details>

## Theory

### The simple version

Stride makes later layers sample the input sparsely, so each extra layer after a stride covers more of the image. The recurrence captures both effects.

### The formula

$$r_\ell = r_{\ell-1} + (k_\ell - 1)\,j_{\ell-1}, \qquad j_\ell = j_{\ell-1}\,s_\ell$$

### How NumPy/PyTorch actually implements this

Receptive-field calculators in CNN tooling use this same recurrence.

## Explanation

The jump is the distance in input pixels between adjacent units, so it is the product of strides so far.
