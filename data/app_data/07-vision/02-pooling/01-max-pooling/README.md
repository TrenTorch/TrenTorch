---
name: vision-pool-max
title: 'Max Pooling: Downsampling by Keeping the Strongest Response'
tags: [computer-vision, pooling]
difficulty: Beginner
---

## Statement

### The problem, from first principles

`01-convolutions/03-stride` showed one way to shrink a feature map: skip positions while still running the full weighted-sum computation at each one. Pooling is a second, even simpler way — instead of a learned weighted sum, just look at a small window and keep the single strongest value in it, throwing the rest away entirely.

The intuition is that a feature map's job is usually to say "how strongly does this pattern show up here" — if it fired strongly ANYWHERE in a small neighborhood, that's usually the information worth keeping, and exactly where within that neighborhood it fired is often noise you can safely discard.

### From theory to code

Theory says: divide the image into small windows (non-overlapping by default), and for each window, keep only its maximum value, once per channel.

Implement `max_pool2d(image, kernel_size, stride=None)` against that reasoning.

### Constraints

- `image`: shape `(C, H, W)`.
- `kernel_size`: the pooling window's height and width.
- `stride`: step between windows; if `None`, defaults to `kernel_size` (non-overlapping pooling).
- Output: shape `(C, (H - kernel_size)//stride + 1, (W - kernel_size)//stride + 1)`.
- Pooling has no learned weights and no bias — it's a pure reduction, applied identically to every channel independently.
- `image` is never modified in place.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

This is the same sliding-window structure as `01-convolutions` — the only thing that changes is what you do with the window: `.max()` instead of elementwise-multiply-and-sum.

</details>

<details>
<summary>Hint 2</summary>

Pool each channel independently: `window.max(axis=(1, 2))` on a `(C, kernel_size, kernel_size)` slice reduces over just the spatial axes, leaving one max per channel in a single call.

</details>

## Theory

### The simple version

Imagine breaking a feature map into small tiles and, for each tile, keeping only the single loudest pixel — the rest of that tile's detail is discarded. If a pattern the network cares about lit up ANYWHERE in that tile, the max survives; the exact pixel-level position within the tile doesn't.

### The formula

```text
output[c, i, j] = max(image[c, i*stride:i*stride+k, j*stride:j*stride+k])
```

for every channel `c` independently. With the default `stride = kernel_size`, windows tile the image with no overlap and no gaps — every input pixel contributes to exactly one output value.

### How PyTorch actually implements this

`torch.nn.functional.max_pool2d(image, kernel_size, stride=None)` computes exactly this (with the identical "stride defaults to kernel_size" convention). Historically, max pooling was the standard downsampling operation between convolutional blocks in architectures like AlexNet and VGG; many modern architectures (ResNet onward) increasingly prefer a strided convolution instead (`01-convolutions/03-stride`), since it lets the network learn how to downsample rather than fixing the rule in advance — but max pooling remains common, especially early in a network and in the final global-pooling step (`03-adaptive-average-pooling`).

## Explanation

The nested loop visits each output position `(i, j)` and slices out `image[:, i*stride:i*stride+k, j*stride:j*stride+k]` — a `(C, k, k)` block across every channel at once. Calling `.max(axis=(1, 2))` reduces over just the two spatial axes, producing one scalar per channel in a single vectorized call rather than looping over channels too — the channel axis is left untouched throughout, which is exactly why pooling never mixes information between channels the way a multi-channel convolution (`01-convolutions/04-multi-channel-input`) deliberately does.
