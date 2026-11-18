---
name: research-nin-global-average-pool
title: 'Network in Network: Global Average Pooling'
tags: [research-papers, architecture, pooling]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Instead of flattening a large feature map into a dense layer with many parameters, the paper averages each channel over space. The result is one number per class-specific channel, with no extra weights.

### From theory to code

Implement `global_average_pool(x)`, which averages an `(H, W, C)` feature map over its spatial dimensions and returns a length-`C` vector.

### Constraints

- Output has shape `(C,)`.

### Hints

<details>
<summary>Hint 1</summary>

Average over axes 0 and 1 together.

</details>

## Theory

### The simple version

Each channel becomes a single score for the whole image. Because the average is over space, the classifier does not depend on where in the image a feature appears.

### The formula

$$\text{GAP}_c = \frac{1}{HW}\sum_{h=1}^{H}\sum_{w=1}^{W} x_{h,w,c}$$

### How NumPy/PyTorch actually implements this

`torch.nn.AdaptiveAvgPool2d(1)` followed by flatten computes the same vector.

## Explanation

The mean over both spatial axes at once is a direct translation of the formula. It has no learnable parameters, which is the point of the design.
