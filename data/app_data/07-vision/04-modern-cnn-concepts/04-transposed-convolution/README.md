---
name: vision-modern-transposed-conv
title: Transposed Convolution
tags: [computer-vision, cnn, upsampling]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

A normal convolution shrinks (or preserves) spatial size — it never grows it. But plenty of tasks need the opposite: semantic segmentation needs a full-resolution output mask from a compressed feature map, and generative models need to turn a small latent representation into a full-size image. Something has to *learnably upsample*, and a transposed convolution is the standard way to do that: instead of sliding a kernel over the input and collapsing a patch into one output value, it takes each single input value and scatters a scaled copy of the kernel outward into the (larger) output.

### From theory to code

Theory says: build an all-zero output big enough to hold every scattered kernel copy, then for every input pixel, add that pixel's value times the kernel into the output window starting at that pixel's (stride-scaled) position — summing wherever windows from different input pixels overlap.

Implement `conv_transpose2d(x, kernel, stride=1)` against that reasoning, for the single-input-channel, single-output-filter case.

### Constraints

- `x`: shape `(1, H, W)`.
- `kernel`: shape `(1, 1, kH, kW)`.
- `stride`: positive integer controlling how far apart, in the output, consecutive input pixels' kernel copies are placed.
- Output shape: `(1, (H - 1) * stride + kH, (W - 1) * stride + kW)`.
- Overlapping contributions from different input pixels are summed, never overwritten.
- `x` and `kernel` are never modified in place.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Compute `out_h = (H - 1) * stride + kH` and `out_w = (W - 1) * stride + kW` first, and allocate a zero array of that size before doing anything else.

</details>

<details>
<summary>Hint 2</summary>

Loop over every input pixel `(i, j)`: the window it contributes to starts at output position `(i * stride, j * stride)` and is `kH` by `kW` in size. Use `+=` (not `=`) so overlapping windows from different input pixels accumulate instead of clobbering each other.

</details>

## Theory

### The simple version

A normal convolution asks, for every output position, "what input patch maps here, and what's the weighted sum of it?" A transposed convolution asks the reverse question, for every *input* position: "what output region does this one value influence, and by how much?" — then it stamps a scaled copy of the kernel into that region for every input pixel, letting overlapping stamps add together. It's not mathematically an inverse of convolution (it doesn't recover the original pre-convolution input), but it does exactly reverse the *shape* change: a convolution that would shrink an image is exactly undone, size-wise, by a transposed convolution with the same kernel size and stride.

### The formula

```text
out_h, out_w = (H-1)*stride + kH, (W-1)*stride + kW
output = zeros(out_h, out_w)
for i in range(H):
    for j in range(W):
        output[i*stride : i*stride+kH, j*stride : j*stride+kW] += x[i, j] * kernel
```

### How PyTorch actually implements this

`torch.nn.ConvTranspose2d` is exactly this operation, generalized to multiple input/output channels, padding, dilation, and `output_padding` (which resolves the ambiguity when several different input sizes could produce the same output size under a given stride). It's the standard upsampling layer in segmentation networks (U-Net's decoder path) and image generators (DCGAN's generator), almost always paired with `BatchNorm2d` and a nonlinearity, exactly like a regular convolution block, just growing spatial size instead of shrinking it.

## Explanation

The output size formula `(H - 1) * stride + kH` falls out directly from where the *last* input pixel's window lands: input pixel `H-1` contributes a window starting at row `(H-1)*stride` and extending `kH` rows further, so the output must be at least that tall to hold it — the `-1` accounts for the very first input pixel needing a window starting at row 0, not row `stride`. The nested loop places one scaled copy of the kernel per input pixel, at a location determined purely by `stride` — using `+=` rather than `=` is what makes overlapping windows (which happen whenever `stride < kernel size`) sum their contributions instead of the later one silently overwriting the earlier one, which is exactly the accumulation behavior a real transposed convolution relies on.
