---
name: research-nin-conv1x1
title: 'Network in Network: The 1x1 Convolution'
tags: [research-papers, architecture, convolution]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Network in Network (Lin, Chen & Yan, 2013) replaces a convolution's linear filter with a small multilayer network applied at every position. A 1x1 convolution is the simplest form: a dense layer over channels, reused at each pixel.

### From theory to code

Implement `conv1x1(x, W, b)`, which maps an `(H, W, C)` feature map to `(H, W, C_out)` with one linear layer per pixel.

### Constraints

- The same `W` and `b` are used at every spatial position.

### Hints

<details>
<summary>Hint 1</summary>

Apply `x @ W.T + b`; NumPy broadcasts the matrix multiply over the first two axes.

</details>

## Theory

### The simple version

A 1x1 kernel looks at one pixel at a time, so it only mixes channels. Repeating the same small network everywhere gives a cheap way to add nonlinearity without a larger receptive field.

### The formula

$$y_{h,w,:} = W\,x_{h,w,:} + b$$

### How NumPy/PyTorch actually implements this

`torch.nn.Conv2d(C, C_out, kernel_size=1)` computes this operation, with channels moved to the front.

## Explanation

The matrix multiply acts on the last axis, so the operation is the same at every `(h, w)`. This is exactly a 1x1 convolution.
