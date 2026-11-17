---
name: research-swish-vs-relu-gap
title: 'Swish: How Close Is It to ReLU?'
tags: [research-papers, activation, swish]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Swish is meant to behave like ReLU where ReLU works well, while staying smooth elsewhere. This question measures how far apart the two curves are, which is the quantity the paper's sharpness parameter controls.

### From theory to code

Implement `swish_relu_gap(x, beta)`, returning the largest absolute difference between `swish(x, beta)` and `relu(x)` over the input values.

### Constraints

- Returns a Python float.

### Hints

<details>
<summary>Hint 1</summary>

Compute both functions over the array, take the absolute difference, then the maximum.

</details>

## Theory

### The simple version

Larger beta makes the sigmoid gate sharper, so Swish approaches ReLU. The gap shrinks as beta grows, which is exactly the behaviour the paper's beta parameter is for.

### The formula

$$\max_x \left|\, x\sigma(\beta x) - \max(x, 0)\,\right|$$

### How NumPy/PyTorch actually implements this

`torch.nn.functional.silu` versus `torch.relu` can be compared the same way on any tensor.

## Explanation

Swish and ReLU differ mostly near zero. The gap is computed directly from the two formulas, with no approximation.
