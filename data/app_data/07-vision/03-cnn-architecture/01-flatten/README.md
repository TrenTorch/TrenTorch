---
name: vision-cnn-flatten
title: 'Flatten: Bridging Convolutional and Linear Layers'
tags: [computer-vision, cnn]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Everything built in `01-convolutions` and `02-pooling` operates on spatial data — arrays shaped `(C, H, W)`, where position matters. `01-classical-ml/01-linear-regression/01-hypothesis-function`'s `linear` operates on the opposite shape of assumption: a flat vector of features, no spatial structure at all. To connect a convolutional feature extractor to a `Linear` classifier head, something has to convert one shape convention into the other — that's flatten's entire job.

### From theory to code

Theory says there's no real computation here, only a reinterpretation: take every value in a `(C, H, W)` array and lay it out as one long 1D vector, in the same order the array is already stored in.

Implement `flatten(image)` against that reasoning.

### Constraints

- `image`: shape `(C, H, W)`.
- Output: shape `(C*H*W,)`.
- Order: channel-major, then row, then column — the same order `image.reshape(-1)` and `torch.flatten` both use by default.
- Every value must be preserved exactly, only the shape changes.
- `image` is never modified in place.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

There's no computation to derive here — this is a single NumPy method call on `image`.

</details>

<details>
<summary>Hint 2</summary>

`.reshape(-1)` collapses every axis into one, in the array's existing memory order — exactly the channel-major, row-major order this question asks for.

</details>

## Theory

### The simple version

Imagine a stack of photographs (the channels), each one made of rows of pixels. Flattening just means reading every pixel off in a fixed order — first photo's pixels, row by row, then the second photo's pixels, and so on — and writing them all into one long list. Nothing about the VALUES changes, only how they're organized.

### The formula

```text
flatten(image)[k] = image[c, h, w]   where k = c*H*W + h*W + w
```

`-1` in `reshape(-1)` tells NumPy to compute the one remaining dimension automatically from the total element count — you don't need to know `C*H*W` up front to use it.

### How PyTorch actually implements this

`torch.flatten(x)` (or `x.view(-1)`, or `nn.Flatten()` as a layer) does exactly this reshape. Inside a real `nn.Module`, `nn.Flatten()` is almost always placed as the last layer before the final classifier `Linear`, converting the convolutional backbone's `(C, H, W)` feature map into the flat vector that layer expects — with the added detail that a real network processes a BATCH of images at once, so the actual call flattens all axes except the batch dimension (`start_dim=1`), a detail this single-image version sidesteps entirely.

## Explanation

`image.reshape(-1)` asks NumPy to produce a view (or copy, only if the data isn't already contiguous) of `image`'s existing memory in one flat dimension, using the array's native row-major storage order — which is precisely channel-major, then row, then column, since that's the order a `(C, H, W)` NumPy array's elements are laid out in memory to begin with. No values move or change; only the shape metadata describing how to read that memory changes.
