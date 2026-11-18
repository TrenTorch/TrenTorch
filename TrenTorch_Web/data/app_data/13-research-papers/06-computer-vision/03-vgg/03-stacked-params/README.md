---
name: research-vgg-stacked-params
title: 'VGG: Parameters of a Stack of Convolutions'
tags: [research-papers, computer-vision, cnn, architecture]
difficulty: Beginner
---

## Statement

### The problem, from first principles

The 3x3 stacking argument is about parameters as well as receptive field. Three 3x3 layers use 27 weights per channel pair, against 49 for a single 7x7 layer, for the same reach.

### From theory to code

Implement `stacked_params(n, c, k)`, the weight count of `n` convolutions with `c` channels each.

### Constraints

- Ignore biases.

### Hints

<details>
<summary>Hint 1</summary>

Multiply the number of layers, the kernel area and the square of the channel count.

</details>

## Theory

### The simple version

For equal channel counts, the 3x3 stack needs 27c^2 weights against 49c^2 for the 7x7 layer, so the stack is cheaper for the same receptive field.

### The formula

$$W = n\,k^2\,c^2$$

### How NumPy/PyTorch actually implements this

Parameter counting utilities compute the same sum from layer shapes.

## Explanation

The comparison is the reason VGG used 3x3 convolutions throughout.
