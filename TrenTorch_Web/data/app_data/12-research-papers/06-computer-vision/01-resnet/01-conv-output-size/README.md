---
name: research-resnet-conv-output-size
title: 'ResNet: The Convolution Output Size'
tags: [research-papers, computer-vision, cnn, architecture]
difficulty: Beginner
---

## Statement

### The problem, from first principles

ResNet (He et al., 2016) opens with a large strided convolution that shrinks the image. Knowing how the spatial size changes at each layer is needed to design such networks and to check their shapes.

### From theory to code

Implement `conv_output_size(n, k, s, p)`, returning the output length of a convolution along one dimension.

### Constraints

- Use integer division.

### Hints

<details>
<summary>Hint 1</summary>

Add the padding on both sides, subtract the kernel, divide by the stride, floor, then add one.

</details>

## Theory

### The simple version

Stride and padding are the two knobs that control downsampling. The ResNet stem uses stride 2 to take a 224 image down to 112 before any residual block.

### The formula

$$n_{\text{out}} = \left\lfloor\frac{n + 2p - k}{s}\right\rfloor + 1$$

### How NumPy/PyTorch actually implements this

Deep learning frameworks compute this in their convolution shape inference using the same expression.

## Explanation

The formula is the same for each spatial dimension; a square image uses it twice.
