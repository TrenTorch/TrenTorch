---
name: vision-conv-multi-channel
title: Convolution over Multi-Channel Input
tags: [computer-vision, convolutions, channels]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`01-single-filter-conv2d` works on one 2D grid of numbers. A real image isn't one grid — a color photo is three (red, green, blue), and every layer past the first in a real CNN outputs dozens or hundreds of feature channels stacked on top of each other. A filter that only understands one channel can't use color information at all, let alone combine features from many channels the way a real network needs to.

The fix is to give the kernel its own 2D slice per input channel, run each channel through its own slice, and combine the per-channel results into one number per position — the filter looks at every channel simultaneously and produces a single, richer output that already accounts for all of them.

### From theory to code

Theory reduces the multi-channel case to something already built: run `01-single-filter-conv2d`'s convolution independently on each channel, using that channel's own kernel slice, then add the per-channel outputs together into one combined result.

Implement `conv2d_multi_channel(image, kernel)` against that reasoning, reusing `conv2d_single_filter` rather than reimplementing the sliding-window logic per channel.

### Constraints

- `image`: shape `(C_in, H, W)`.
- `kernel`: shape `(C_in, kH, kW)` — one 2D filter per input channel.
- Output: shape `(H - kH + 1, W - kW + 1)`, a single 2D result, summed across channels.
- `C_in = 1` must reduce exactly to `01-single-filter-conv2d`'s behavior.
- `image` and `kernel` are never modified in place.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Loop over the channel axis. For channel `c`, `image[c]` and `kernel[c]` are each plain 2D arrays — exactly what `conv2d_single_filter` from `01-single-filter-conv2d` already expects.

</details>

<details>
<summary>Hint 2</summary>

Accumulate: start an output array of zeros with the right shape, then add each channel's `conv2d_single_filter(image[c], kernel[c])` result into it.

</details>

## Theory

### The simple version

Imagine three separate stencils — one tuned for red patterns, one for green, one for blue — all stacked and applied to the same position on a color photo at once, then their three individual readings added together into one combined number. The result reflects all three color channels' worth of information, collapsed into a single value per position.

### The formula

```text
output[i, j] = sum over c of sum(image[c, i:i+kH, j:j+kW] * kernel[c])
             = sum over c of conv2d_single_filter(image[c], kernel[c])[i, j]
```

Summing across channels, rather than keeping them separate, is exactly why one filter can combine information from every input channel into a single, richer output — the filter genuinely SEES all channels together, not one at a time in isolation.

### How PyTorch actually implements this

`torch.nn.functional.conv2d(image, kernel)`, where `image` has shape `(C_in, H, W)` and `kernel` has shape `(C_in, kH, kW)` (or `(1, C_in, kH, kW)` once batch/output-filter dimensions are added in `05-multiple-output-filters`), computes exactly this per-channel-then-sum operation internally — it's the reason a convolutional layer's weight count scales with `C_in`, not just kernel size, since it genuinely needs one full 2D filter per input channel.

## Explanation

The loop over `range(C_in)` calls `conv2d_single_filter(image[c], kernel[c])` once per channel — each call is completely independent, using only that channel's own slice of the kernel, and reuses the exact sliding-window logic from `01-single-filter-conv2d` unchanged. Accumulating into `output` with `+=` sums those per-channel 2D results elementwise, which is mathematically identical to summing over `c` inside the sliding-window loop itself — this two-step (per-channel convolve, then sum) structure is just an easier-to-verify way of writing the same computation, not a different one.
