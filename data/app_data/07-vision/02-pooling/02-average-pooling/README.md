---
name: vision-pool-average
title: 'Average Pooling: Downsampling by Smoothing Instead of Selecting'
tags: [computer-vision, pooling]
difficulty: Beginner
---

## Statement

### The problem, from first principles

`01-max-pooling` keeps only a window's single loudest value, discarding everything else outright — a deliberate, sometimes aggressive choice. Average pooling makes the opposite choice: instead of picking a winner, it blends every value in the window into one smoothed number, so a single unusually large or small pixel doesn't dominate the result the way it would under max pooling.

Both are valid ways to shrink a feature map; which one helps depends on whether you want the network to notice "did this pattern fire strongly anywhere" (max) or "what's the overall level of activity here" (average).

### From theory to code

Theory changes exactly one operation from `01-max-pooling`: replace the per-window maximum with the per-window mean. Everything about how windows are laid out and stepped through stays identical.

Implement `avg_pool2d(image, kernel_size, stride=None)` against that reasoning.

### Constraints

- `image`: shape `(C, H, W)`.
- `kernel_size`: the pooling window's height and width.
- `stride`: step between windows; if `None`, defaults to `kernel_size` (non-overlapping pooling).
- Output: shape `(C, (H - kernel_size)//stride + 1, (W - kernel_size)//stride + 1)`.
- Every value inside a window contributes equally to that window's output — no weighting, no learned parameters.
- `image` is never modified in place.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

This is `01-max-pooling` with one line changed: `.mean(axis=(1, 2))` instead of `.max(axis=(1, 2))` on each window.

</details>

<details>
<summary>Hint 2</summary>

`window.mean(axis=(1, 2))` on a `(C, kernel_size, kernel_size)` slice reduces over just the spatial axes in one call, leaving one averaged value per channel.

</details>

## Theory

### The simple version

Where max pooling asks "what's the strongest signal in this patch?", average pooling asks "what's the typical signal in this patch?" — every pixel gets an equal vote, and the result is a smoothed, less spiky summary of the region rather than a single stand-out value.

### The formula

```text
output[c, i, j] = mean(image[c, i*stride:i*stride+k, j*stride:j*stride+k])
```

for every channel `c` independently, with the same default `stride = kernel_size` non-overlapping tiling `01-max-pooling` uses.

### How PyTorch actually implements this

`torch.nn.functional.avg_pool2d(image, kernel_size, stride=None)` computes exactly this. Average pooling shows up throughout classic CNNs, and its extreme case — pooling an entire feature map down to one value per channel — is important enough to get its own dedicated operation, covered next in `03-adaptive-average-pooling`.

## Explanation

The nested loop visits each output position and slices `image[:, i*stride:i*stride+k, j*stride:j*stride+k]`, exactly as `01-max-pooling` does — the only change is `.mean(axis=(1, 2))` in place of `.max(axis=(1, 2))`, reducing over the two spatial axes while leaving the channel axis untouched. Because every value in the window contributes equally to the mean, a single extreme pixel has far less influence on the output than it would under max pooling, where one large value alone determines the entire result — this is the concrete, mechanical reason the two operations behave so differently on the same input.
