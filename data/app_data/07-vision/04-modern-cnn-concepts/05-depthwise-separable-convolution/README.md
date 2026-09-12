---
name: vision-modern-depthwise-separable
title: Depthwise-Separable Convolution
tags: [computer-vision, cnn, efficiency]
difficulty: Advanced
---

## Statement

### The problem, from first principles

A regular `(C_out, C_in, kH, kW)` convolution does two jobs at once, every single output pixel: it looks at a spatial neighborhood (spatial filtering) *and* it combines every input channel together (channel mixing). Doing both jobs simultaneously means the cost scales with `C_out * C_in * kH * kW` — with enough channels, that's the majority of the compute in a modern CNN. Depthwise-separable convolution asks: what if these two jobs were split into two separate, much cheaper steps instead of one expensive combined one?

### From theory to code

Theory says: first, filter each input channel completely independently with its own small spatial kernel (the "depthwise" stage — no channel mixing at all, reusing `01-single-filter-conv2d`). Then, mix the resulting channels together with a 1x1 convolution (the "pointwise" stage — no spatial filtering at all, reusing `03-1x1-convolution`). Chaining these two cheap stages approximates what one expensive full convolution would have done, at a fraction of the compute.

Implement `depthwise_separable_conv2d(x, depthwise_kernel, pointwise_kernel)` against that reasoning.

### Constraints

- `x`: shape `(C_in, H, W)`.
- `depthwise_kernel`: shape `(C_in, 1, kH, kW)` — exactly one spatial filter per input channel, applied to that channel only.
- `pointwise_kernel`: shape `(C_out, C_in, 1, 1)` — mixes the depthwise stage's channels into `C_out` output channels.
- Returns shape `(C_out, H - kH + 1, W - kW + 1)`.
- `x`, `depthwise_kernel` and `pointwise_kernel` are never modified in place.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

The depthwise stage is a plain Python loop: `[conv2d_single_filter(x[c], depthwise_kernel[c, 0]) for c in range(C_in)]`, one independent 2D convolution per channel with no interaction between channels.

</details>

<details>
<summary>Hint 2</summary>

`np.stack(...)` the list of per-channel depthwise outputs back into one `(C_in, H', W')` array, then pass that straight into `pointwise_conv` with `pointwise_kernel` to get the final `(C_out, H', W')` result.

</details>

## Theory

### The simple version

Think of a regular convolution as one person doing two jobs at once for every output pixel: "look at this neighborhood AND combine every channel's opinion." Depthwise-separable convolution splits this into an assembly line: first, `C_in` specialists each independently filter their own single channel spatially (nobody talks to anybody else's channel), then one 1x1 convolution acts like a manager who takes all those independent per-channel opinions and blends them into the final answer. Two cheap, focused steps replace one expensive, combined one.

### The formula

```text
depth_out[c] = conv2d_single_filter(x[c], depthwise_kernel[c, 0])   # per channel, independent
depth_out    = stack(depth_out)                                     # (C_in, H', W')
out          = pointwise_conv(depth_out, pointwise_kernel)          # mix channels -> (C_out, H', W')
```

### How PyTorch actually implements this

`torch.nn.Conv2d(C_in, C_in, kernel_size, groups=C_in)` followed by `torch.nn.Conv2d(C_in, C_out, kernel_size=1)` implements exactly this two-stage pattern — the `groups=C_in` argument is what tells a regular `Conv2d` to apply one filter per channel with no cross-channel mixing, instead of the default fully-mixed behavior. This is the core building block of MobileNet and similar architectures designed to run on phones and other compute-constrained hardware: for a `3x3` kernel with 256 channels, depthwise-separable convolution uses roughly 8-9x fewer multiply-adds than a regular convolution doing the same channel counts, at the cost of being a strictly less expressive family of functions (it can't represent every possible full convolution).

## Explanation

The list comprehension `[conv2d_single_filter(x[c], depthwise_kernel[c, 0]) for c in range(C_in)]` runs `C_in` completely independent single-channel convolutions — `depthwise_kernel[c, 0]` is channel `c`'s own `(kH, kW)` filter, and `conv2d_single_filter` never sees any other channel, so no cross-channel mixing happens at this stage. `np.stack` reassembles these `C_in` independent `(H', W')` results back into one `(C_in, H', W')` array, restoring the channel axis that the per-channel loop had temporarily discarded. Feeding that into `pointwise_conv` with `pointwise_kernel` performs the channel-mixing job on its own, exactly as in `03-1x1-convolution` — the two stages together produce the same `(C_out, H', W')` shape a full convolution would have, using far fewer multiply-adds because neither stage does both jobs (spatial filtering and channel mixing) at once.
