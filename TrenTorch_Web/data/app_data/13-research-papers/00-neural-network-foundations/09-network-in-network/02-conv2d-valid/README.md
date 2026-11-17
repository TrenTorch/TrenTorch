---
name: research-nin-conv2d-valid
title: 'Network in Network: A Valid 2D Convolution'
tags: [research-papers, architecture, convolution]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

The paper's micronetworks sit on top of ordinary spatial convolutions. This question implements that spatial part directly, so the 1x1 layers from the previous question have something to act on.

### From theory to code

Implement `conv2d_valid(img, kernel)`, which slides the kernel over the image with no padding and returns the sums of elementwise products.

### Constraints

- Output size is `(H - kh + 1, W - kw + 1)`.
- This is cross-correlation: the kernel is not flipped.

### Hints

<details>
<summary>Hint 1</summary>

Use two loops over output positions and sum the elementwise product of each window with the kernel.

</details>

## Theory

### The simple version

Each output pixel is a weighted sum of the window beneath it. Without padding the output shrinks by the kernel size minus one in each dimension.

### The formula

$$y_{i,j} = \sum_{u,v} x_{i+u,\,j+v}\,k_{u,v}$$

### How NumPy/PyTorch actually implements this

`torch.nn.functional.conv2d` with `padding=0` and single channels computes the same valid output.

## Explanation

Deep learning convolutions use cross-correlation: the kernel is applied without flipping. The double loop mirrors the formula, though vectorized code is faster.
