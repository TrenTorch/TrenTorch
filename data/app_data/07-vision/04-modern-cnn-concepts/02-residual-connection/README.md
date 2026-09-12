---
name: vision-modern-residual-block
title: Residual (Skip) Connection
tags: [computer-vision, cnn, architecture]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Stacking more convolutional layers should let a network learn richer features — but past a certain depth, plain stacks of convolutions actually get *harder* to train, not easier: gradients have to flow back through every layer, and if a layer's Jacobian shrinks the gradient even slightly, dozens of layers compound that shrinkage until the earliest layers barely learn at all. A residual (skip) connection sidesteps this by adding a layer's input directly to its output, giving the gradient a direct, unobstructed path backward through the addition, regardless of how the convolution in between behaves.

### From theory to code

Theory says: run the input through a convolution that is padded so its output has the exact same shape as the input, add the original input back to that convolution's output, then apply a nonlinearity. The network only has to learn a "residual" correction on top of the identity — if the best thing to do is nothing at all, it just has to learn to output all zeros from the convolution.

Implement `residual_block(x, kernel)` against that reasoning, reusing the existing multi-filter convolution and ReLU.

### Constraints

- `x`: shape `(C, H, W)` — a single feature map, no batch dimension.
- `kernel`: shape `(C, C, 3, 3)` — same number of output channels as input channels, since the result must be addable back to `x`.
- Padding must be exactly 1 pixel on every side of `H` and `W`, so a 3x3 convolution leaves the spatial size unchanged.
- Returns an array the same shape as `x`.
- `x` and `kernel` are never modified in place.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`np.pad(x, ((0, 0), (1, 1), (1, 1)))` pads only the height and width axes by 1, leaving the channel axis untouched — exactly what a "same"-padded 3x3 convolution needs.

</details>

<details>
<summary>Hint 2</summary>

Run `conv2d_multi_filter` on the *padded* input, but add the result to the *original, unpadded* `x` — then pass that sum through `relu_forward`.

</details>

## Theory

### The simple version

Think of a residual block as a note passed alongside the main computation: "here's the original input, in case the transformation in between doesn't help." Instead of forcing every layer to invent a completely new representation from scratch, the network can default to passing the input straight through (identity) and only spend effort learning a small correction on top — which turns out to be a dramatically easier optimization problem than learning the whole transformation directly.

### The formula

```text
padded    = pad(x, 1 pixel on each side of H and W)
conv_out  = conv2d_multi_filter(padded, kernel)   # same shape as x
out       = relu(x + conv_out)
```

### How PyTorch actually implements this

This is the core building block of ResNet (`torchvision.models.resnet18` and friends): each residual block is `nn.Sequential(conv, batchnorm, relu, conv, batchnorm)` wrapped so its output is added to its own input before a final `relu`, exactly as above but usually with two convolutions instead of one and a `BatchNorm2d` after each. When the input and output channel counts differ, real ResNets insert a small 1x1 convolution ("projection shortcut") on the skip path itself so the shapes still match for the addition — this exercise sidesteps that by requiring `kernel`'s input and output channel counts to be equal.

## Explanation

`np.pad(x, ((0, 0), (1, 1), (1, 1)))` adds one row/column of zeros on every side of the height and width axes (and none on the channel axis), which is exactly what "same" padding for a 3x3 kernel requires — running `conv2d_multi_filter` on this padded input produces an output with the identical `(C, H, W)` shape as the original `x`. Adding the *original, unpadded* `x` back to that convolution output is the skip connection itself: the network's job becomes learning `conv_out` as a correction on top of `x`, rather than reconstructing `x`'s useful information from scratch. The final `relu_forward` on the sum introduces the nonlinearity a stack of these blocks needs to represent more than a linear function overall.
