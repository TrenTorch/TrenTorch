---
name: research-vgg-receptive-field
title: 'VGG: Receptive Field of Stacked 3x3 Convolutions'
tags: [research-papers, computer-vision, cnn, architecture]
difficulty: Beginner
---

## Statement

### The problem, from first principles

VGG (Simonyan & Zisserman, 2014) replaced large filters with stacks of 3x3 convolutions. Three 3x3 layers see the same area as one 7x7 layer, with fewer parameters and more non-linearities.

### From theory to code

Implement `receptive_field_stack(n, k)`, the receptive field of a stack of `n` convolutions with kernel `k`.

### Constraints

- Stride one, as in the paper's stacks.

### Hints

<details>
<summary>Hint 1</summary>

Each extra layer adds `k - 1` pixels to the field, starting from one pixel.

</details>

## Theory

### The simple version

A deep stack of small kernels covers a large region while keeping the parameter count low and inserting a ReLU after every layer.

### The formula

$$R = 1 + n\,(k - 1)$$

### How NumPy/PyTorch actually implements this

Receptive field calculators in model analysis tools apply the same recurrence.

## Explanation

Three stacked 3x3 layers give a 7x7 field, which the paper uses to justify the design.
