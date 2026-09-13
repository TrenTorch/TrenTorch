---
name: vision-modern-pointwise-conv
title: 1x1 Convolution (Bottleneck)
tags: [computer-vision, cnn, architecture]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Every convolution seen so far mixes information across a spatial neighborhood — a 3x3 kernel looks at a 3x3 patch. A 1x1 kernel is the degenerate case: it looks at exactly one pixel, so it can never mix spatial information at all. That sounds useless, but it does something else that's extremely valuable: it mixes information _across channels_ at each pixel independently, letting a network cheaply change how many channels it's carrying (e.g. compress 256 channels down to 64 — a "bottleneck") without touching the spatial structure at all.

### From theory to code

Theory says: since a 1x1 convolution never looks past a single pixel, every output pixel is just a fixed linear combination of that same pixel's input channels — the exact same `(C_out, C_in)` weight matrix applied at every spatial location. That means the whole operation can be done as one reshape and one matrix multiply, with no loop over spatial positions at all.

Implement `pointwise_conv(x, kernel)` against that reasoning.

### Constraints

- `x`: shape `(C_in, H, W)`.
- `kernel`: shape `(C_out, C_in, 1, 1)`.
- Returns shape `(C_out, H, W)` — same spatial size as `x`, remapped channel count.
- `x` and `kernel` are never modified in place.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`kernel.reshape(C_out, C_in)` squeezes away the two trailing size-1 dimensions, turning the 1x1 conv kernel into a plain weight matrix.

</details>

<details>
<summary>Hint 2</summary>

`x.reshape(C_in, H * W)` turns every pixel's channel vector into one column of a `(C_in, H*W)` matrix — `weight @ x_flat` then applies the same linear map to every column (every pixel) at once. Reshape the `(C_out, H*W)` result back to `(C_out, H, W)`.

</details>

## Theory

### The simple version

Picture every pixel in the image as carrying its own little vector of `C_in` numbers (one per channel). A 1x1 convolution doesn't care where that pixel is or what its neighbors look like — it just takes that one pixel's channel vector and runs it through the exact same small linear layer (weight matrix) as every other pixel, producing a new vector of `C_out` numbers for that pixel. Do this independently for all `H*W` pixels and you've "convolved" with a 1x1 kernel.

### The formula

```text
weight  = kernel.reshape(C_out, C_in)     # squeeze the 1x1 spatial dims away
x_flat  = x.reshape(C_in, H * W)          # every pixel becomes one column
out     = (weight @ x_flat).reshape(C_out, H, W)
```

### How PyTorch actually implements this

`torch.nn.Conv2d(C_in, C_out, kernel_size=1)` is a completely ordinary convolution layer as far as PyTorch's API is concerned — there's no special case in the code path. But architecturally, 1x1 convolutions are everywhere: ResNet's "bottleneck" blocks use one 1x1 conv to shrink channel count before an expensive 3x3 conv and another to expand it back afterward, and Inception-style networks use 1x1 convolutions purely to control channel count cheaply between more expensive operations. The next question in this track, depthwise-separable convolution, uses exactly this `pointwise_conv` as its second stage.

## Explanation

`kernel.reshape(C_out, C_in)` is valid precisely because the kernel's last two dimensions are both 1 — reshaping doesn't reorder any values, it just drops the two size-1 axes, leaving a genuine `(C_out, C_in)` weight matrix. `x.reshape(C_in, H * W)` flattens the spatial grid into a single axis, so column `k` of the result is exactly the `C_in`-length channel vector that used to live at spatial position `k` — reshape preserves this because both `x` and the flattened axis iterate over `(H, W)` in the same row-major order. `weight @ x_flat` then applies the identical `(C_out, C_in)` linear map to every column (every pixel) simultaneously, which is exactly "the same 1x1 kernel at every spatial position" — reshaping the `(C_out, H*W)` result back to `(C_out, H, W)` restores the spatial grid, now with `C_out` channels instead of `C_in`.
