---
name: vision-conv-single-filter
title: Single-Channel, Single-Filter 2D Convolution
tags: [computer-vision, convolutions]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

A `Linear` layer treats every input feature as independent — pixel (0, 0) and pixel (50, 50) get their own separate weight, with no notion that they're spatially near anything. That throws away the one fact that makes an image an image: nearby pixels are related, and the same small visual pattern (an edge, a corner) can show up anywhere in the frame.

A convolution fixes this by sliding one small, shared set of weights (a kernel) across every position in the image, computing the same local weighted sum wherever it lands. The same edge-detector kernel that works in the top-left corner works, unchanged, in the bottom-right — one small parameter set, reused everywhere, instead of one giant one used nowhere twice.

### From theory to code

Theory reduces this to one repeated operation: at every valid position, take the image patch directly under the kernel, multiply elementwise, and sum — a single number per position. Doing that at every position an unshifted kernel still fully overlaps the image (no padding yet, that's the next question) produces the whole output.

Implement `conv2d_single_filter(image, kernel)` against that reasoning. The signature and docstring are already in the editor.

### Constraints

- `image`: shape `(H, W)`.
- `kernel`: shape `(kH, kW)`.
- Output: shape `(H - kH + 1, W - kW + 1)` — "valid" convolution, no padding.
- This is cross-correlation, not textbook (flipped-kernel) convolution — matches what every deep learning framework calls "conv." Do not flip the kernel.
- `image` and `kernel` are never modified in place.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

The output size shrinks because the kernel can't hang off the edge of the image — a `(kH, kW)` kernel has exactly `H - kH + 1` valid row positions to sit in.

</details>

<details>
<summary>Hint 2</summary>

For output position `(i, j)`, the corresponding image patch is `image[i : i+kH, j : j+kW]` — same top-left indexing you'd use to slice out any other sub-block.

</details>

<details>
<summary>Hint 3</summary>

`np.sum(patch * kernel)` is the entire computation for one output position. There's no matrix multiply here — just elementwise multiply, then sum everything.

</details>

## Theory

### The simple version

Imagine sliding a small transparent stencil over a photo, one position at a time. At each position, you multiply whatever's showing through the stencil by the numbers printed on it, add those products up, and write down the single result. Slide the stencil to every position it fits, and the sequence of results is the convolution's output — a new, smaller image, one number per stencil position.

### The formula

```text
output[i, j] = sum over (di, dj) of image[i + di, j + dj] * kernel[di, dj]
             = sum(image[i:i+kH, j:j+kW] * kernel)
```

for every `i` in `0 .. H-kH` and `j` in `0 .. W-kW`. No kernel flip: this is cross-correlation, which is what `torch.nn.functional.conv2d` actually computes despite the name — genuine flipped-kernel convolution is a signal-processing convention deep learning never bothered adopting, since the kernel's weights are learned either way.

### How PyTorch actually implements this

`torch.nn.functional.conv2d(image, kernel)` computes exactly this operation (generalized to batches, channels and multiple filters — the next several questions add each of those one at a time). Real implementations never use the direct nested-loop approach used here; `06-im2col-optimization` shows the actual trick (reshaping the sliding-window patches into one big matrix and using a single matmul) that real libraries use to make this fast on real hardware.

## Explanation

The nested loop walks every valid `(i, j)` output position directly, since there are only `H - kH + 1` times `W - kW + 1` of them and each one needs its own patch of `image`. `image[i : i + kH, j : j + kW]` slices out exactly the region the kernel currently overlaps; multiplying that elementwise by `kernel` and summing computes the single weighted-sum output value for that position, with no kernel flip — the value written at `output[i, j]` is a direct, unflipped cross-correlation, matching what `torch.nn.functional.conv2d` produces exactly.
