---
name: vision-conv-stride
title: 'Stride: Skipping Positions to Downsample'
tags: [computer-vision, convolutions, stride]
difficulty: Beginner
---

## Statement

### The problem, from first principles

`01-single-filter-conv2d` moves the kernel one pixel at a time — every output position overlaps heavily with its neighbors, since a `3x3` kernel shares two full rows/columns with the position right next to it. That's a lot of redundant computation if what you actually want is a smaller output, not a full-resolution one.

Stride is the fix: instead of moving the kernel by 1 pixel between outputs, move it by `stride` pixels. A stride of 2 skips every other position, roughly halving the output's height and width for free — a cheap way to downsample an image while still applying a learned filter to it, which is exactly how many real CNNs shrink spatial size between blocks instead of using a separate pooling layer.

### From theory to code

Theory changes exactly one thing from `01-single-filter-conv2d`: the step between consecutive output positions. Output index `i` now corresponds to image row `i * stride`, not row `i` — everything else about computing one output value (patch, elementwise multiply, sum) stays identical.

Implement `conv2d_with_stride(image, kernel, stride=1)` against that reasoning.

### Constraints

- `image`: shape `(H, W)`. `kernel`: shape `(kH, kW)`. `stride`: positive integer.
- Output shape: `((H - kH) // stride + 1, (W - kW) // stride + 1)`.
- `stride=1` must match `01-single-filter-conv2d` exactly.
- No padding — this question is stride only, `02-padding`'s padding modes aren't part of this contract.
- `image` and `kernel` are never modified in place.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Output position `(i, j)` no longer maps to image position `(i, j)` — it maps to `(i * stride, j * stride)`. Everything else about extracting the patch and summing stays the same.

</details>

<details>
<summary>Hint 2</summary>

The output size formula changes too: with `stride=1` you had `H - kH + 1` valid positions; with a larger stride you only visit every `stride`-th one of those, giving `(H - kH) // stride + 1`.

</details>

## Theory

### The simple version

Instead of sliding your stencil across a photo one pixel at a time, you now hop it across in bigger jumps — landing on every 2nd position, say, instead of every single one. You get fewer results, spread further apart, but each individual result is computed exactly the same way as before.

### The formula

```text
output[i, j] = sum(image[i*stride : i*stride+kH, j*stride : j*stride+kW] * kernel)
```

for `i` in `0 .. (H-kH)//stride` and `j` in `0 .. (W-kW)//stride`. Setting `stride=1` recovers `01-single-filter-conv2d`'s formula exactly, since `i*1 = i`.

### How PyTorch actually implements this

`torch.nn.functional.conv2d(image, kernel, stride=2)` (or any stride value) computes exactly this. Many real architectures use a strided convolution as their downsampling layer instead of a separate pooling operation (`02-pooling`'s topic) — ResNet's very first layer, for instance, is a `stride=2` convolution, combining feature extraction and downsampling into one operation instead of two.

## Explanation

The only change from `01-single-filter-conv2d` is multiplying the output index by `stride` before slicing: `image[i*stride : i*stride+kH, j*stride : j*stride+kW]` instead of `image[i:i+kH, j:j+kW]`. The output size formula `(H - kH) // stride + 1` falls out of counting how many multiples of `stride`, starting from 0, still leave room for a full `kH`-tall patch — the largest valid starting row is `H - kH`, and `(H - kH) // stride` counts how many stride-steps fit into that range, plus the starting position itself.
