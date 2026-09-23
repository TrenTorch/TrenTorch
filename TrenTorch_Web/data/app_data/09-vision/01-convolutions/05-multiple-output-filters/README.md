---
name: vision-conv-multi-filter
title: Multiple Output Filters
tags: [computer-vision, convolutions, channels]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`04-multi-channel-input` combines every input channel into a single output number per position — one filter, one "opinion" about what's at each location. A real convolutional layer never stops at one opinion: it applies many independent filters to the same input at once, each one free to learn a different pattern (one might respond to vertical edges, another to a particular color blob), producing many output channels instead of one.

This is the last piece needed to reach `torch.nn.functional.conv2d`'s actual signature: many input channels in, many output channels out, each output channel its own independent multi-channel filter over the same input.

### From theory to code

Theory says nothing new mathematically — it's `04-multi-channel-input`'s exact computation, run once per output filter, with the results stacked along a new leading axis.

Implement `conv2d_multi_filter(image, kernel)` against that reasoning, reusing `conv2d_multi_channel` rather than reimplementing anything.

### Constraints

- `image`: shape `(C_in, H, W)`.
- `kernel`: shape `(C_out, C_in, kH, kW)` — `C_out` independent filters, each shaped like `04-multi-channel-input`'s kernel.
- Output: shape `(C_out, H - kH + 1, W - kW + 1)`.
- `C_out = 1` must reduce exactly to `04-multi-channel-input`'s output, with a leading size-1 axis.
- `image` and `kernel` are never modified in place.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Loop over the first axis of `kernel` (size `C_out`). Each `kernel[f]` is a `(C_in, kH, kW)` array — exactly what `04-multi-channel-input`'s `conv2d_multi_channel` expects.

</details>

<details>
<summary>Hint 2</summary>

Allocate the output as `(C_out, H_out, W_out)` up front and assign into `output[f]` for each filter, rather than building a Python list and stacking at the end — either works, but preallocating keeps the shape contract explicit.

</details>

## Theory

### The simple version

Instead of one stencil scanning a photo, imagine a whole stack of differently-tuned stencils scanning the same photo in parallel — one tuned to find edges, another to find a particular texture, another something else entirely. Each stencil produces its own full result image; stack all those result images together and that's the multi-filter output.

### The formula

```text
output[f] = conv2d_multi_channel(image, kernel[f])    for f = 0 .. C_out-1
```

Every output channel is computed completely independently of every other — filter `f`'s result never depends on any other filter's weights, only on the shared input `image`.

### How PyTorch actually implements this

`torch.nn.functional.conv2d(image, kernel)` with `image` shape `(N, C_in, H, W)` and `kernel` shape `(C_out, C_in, kH, kW)` computes exactly this (generalized to a batch of images at once — `N` isn't part of this question's contract, but the per-image computation is identical). This is the actual weight tensor shape stored inside every real `torch.nn.Conv2d` layer: `(out_channels, in_channels, kernel_size, kernel_size)`, and `06-im2col-optimization` shows how real hardware runs all `C_out` filters as one single matrix multiply instead of a Python loop over filters.

## Explanation

The loop over `range(C_out)` calls `conv2d_multi_channel(image, kernel[f])` once per filter — each call sees the full input `image` but only that filter's own `(C_in, kH, kW)` weights, so the `C_out` results are entirely independent of each other and can be computed in any order. Writing each result into `output[f]` stacks them along a new leading axis, producing the `(C_out, H_out, W_out)` shape a real convolutional layer's output actually has — one full feature map per learned filter.
