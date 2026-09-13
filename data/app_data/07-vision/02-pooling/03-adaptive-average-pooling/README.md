---
name: vision-pool-adaptive-average
title: 'Adaptive Average Pooling: The Modern Flatten Replacement'
tags: [computer-vision, pooling, global-average-pooling]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`02-average-pooling` needs a fixed `kernel_size` chosen to match a specific input size. But a real classifier's final layers need a FIXED-size feature vector regardless of the input image's resolution — a `224x224` photo and a `256x256` photo should both end up feeding the same-sized `Linear` layer. Adaptive pooling flips the question around: instead of "pool with this window size," it asks "give me exactly THIS output size, whatever window size that takes."

Its most common special case — pooling every channel all the way down to a single number — is the modern replacement for flattening a whole feature map before the final classifier: instead of a huge, resolution-dependent flatten, one number per channel, always, no matter the input size.

### From theory to code

Theory says: for each output cell, figure out which region of the input it's responsible for (a formula, not a fixed window size), and average that region. The region boundaries are computed from `output_size` and the input's actual `H`, `W` — they aren't given directly the way `kernel_size` was in `02-average-pooling`.

Implement `adaptive_avg_pool2d(image, output_size=(1, 1))` against that reasoning.

### Constraints

- `image`: shape `(C, H, W)`.
- `output_size`: `(out_h, out_w)` — the exact output spatial shape to produce.
- Output: shape `(C, out_h, out_w)`.
- `output_size == (1, 1)` (the global-average-pooling case) must average every pixel in each channel exactly once.
- `output_size` equal to the input's own `(H, W)` must be the identity (every output cell covers exactly one input pixel).
- `image` is never modified in place.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

For output row `i` (out of `out_h` total), the input rows it should cover start at `(i * H) // out_h` and end at `ceil((i + 1) * H / out_h)` — the same idea applies to columns with `out_w`, `W`.

</details>

<details>
<summary>Hint 2</summary>

`ceil(a / b)` for positive integers can be computed without floating point as `-(-a // b)` — negate, floor-divide, negate again.

</details>

<details>
<summary>Hint 3</summary>

When `H` divides evenly by `out_h`, every region ends up the same fixed size — in that special case this reduces exactly to `02-average-pooling`'s fixed-window pooling.

</details>

## Theory

### The simple version

Instead of deciding the window size up front and letting the output size fall out of it (regular pooling), you decide the OUTPUT size up front and let each window's size be whatever it needs to be to divide the input evenly into that many pieces. Ask for a `1x1` output and every pixel in the image gets folded into one single average — a global summary of the whole feature map, one number per channel.

### The formula

```text
row_start = (i * H) // out_h
row_end   = ceil((i + 1) * H / out_h)
col_start = (j * W) // out_w
col_end   = ceil((j + 1) * W / out_w)
output[c, i, j] = mean(image[c, row_start:row_end, col_start:col_end])
```

This formula guarantees every input pixel falls into exactly one output cell's region (the regions partition the input completely, with no gaps and no overlap), even when `H` doesn't divide evenly by `out_h` — some regions just end up one pixel larger than others.

### How PyTorch actually implements this

`torch.nn.functional.adaptive_avg_pool2d(image, output_size)` computes exactly this region formula. `nn.AdaptiveAvgPool2d((1, 1))` followed by a flatten is the standard final step in nearly every modern CNN classifier (ResNet, EfficientNet, and beyond) — it replaces the old approach of flattening a fixed-size feature map directly into a huge `Linear` layer, which broke the moment input resolution changed. Global average pooling makes the whole network resolution-independent: the same trained weights work on any input size, since the final feature vector's length depends only on the channel count, never on `H` or `W`.

## Explanation

The region-boundary formula treats `output_size` as fixed and derives each cell's input region from it, rather than the other way around — `row_start = (i * H) // out_h` finds where region `i` begins by proportionally scaling `i` into the `H`-pixel range, and `row_end = ceil((i+1) * H / out_h)` finds where the NEXT region would begin, rounded up so no input row is ever skipped. Averaging over that `image[:, row_start:row_end, col_start:col_end]` slice, per channel, is exactly `02-average-pooling`'s reduction — the only real difference in this question is that the window boundaries come from a formula instead of being handed in directly, which is precisely what lets the same function handle any input resolution while always producing the requested output shape.
