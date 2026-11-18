---
name: research-maxout-relu
title: 'Maxout Networks: ReLU Is a Maxout'
tags: [research-papers, activation, maxout]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Maxout generalizes ReLU: a maxout unit with two pieces, one fixed at zero and one free, reproduces ReLU exactly. The paper uses this to show maxout is at least as expressive as the standard activation.

### From theory to code

Implement `relu_via_maxout(x)`, which returns `max(x, 0)` by taking the maximum of the two pieces `x` and `0`.

### Constraints

- Result must equal `np.maximum(x, 0)`.

### Hints

<details>
<summary>Hint 1</summary>

Stack `x` and an all-zero array along a new last axis, then take the max over that axis.

</details>

## Theory

### The simple version

A maxout unit with pieces `(w x + b)` and `0` is `max(w x + b, 0)`. Setting `w = 1, b = 0` gives ReLU, so ReLU is a special case of maxout.

### The formula

$$\max(x, 0) = \max\big(\underbrace{1 \cdot x + 0}_{\text{piece } 1},\ \underbrace{0 \cdot x + 0}_{\text{piece } 2}\big)$$

### How NumPy/PyTorch actually implements this

`torch.relu` is the built-in; the maxout form shows the same function as a special case of a learned layer.

## Explanation

Stacking the two pieces and taking the max is the maxout operation; the result matches ReLU exactly, element by element.
