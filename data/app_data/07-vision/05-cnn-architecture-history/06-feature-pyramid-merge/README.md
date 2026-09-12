---
name: vision-history-feature-pyramid-merge
title: "Note: Feature Pyramids — Combining Multiple Resolutions"
tags: [computer-vision, cnn, history, detection]
difficulty: Beginner
---

## Statement

### The problem, from first principles

A CNN backbone naturally produces a stack of feature maps at shrinking resolutions as it goes deeper: early layers have high spatial resolution but only simple, low-level features (edges, colors); late layers have low spatial resolution but rich, high-level, semantically meaningful features (object parts, whole shapes). Object detection needs BOTH at once — precise spatial localization (which the early layers have) and confident semantic understanding of what's actually there (which only the late layers have). A Feature Pyramid Network (FPN) solves this by explicitly merging a late, low-resolution layer's features back into an earlier, high-resolution layer, combining the strengths of both.

### From theory to code

Theory says: to merge a high-resolution, low-level feature map with a low-resolution, high-level one, first upsample the low-resolution map so its spatial size matches the high-resolution one (FPN uses simple nearest-neighbor upsampling, not a learned transposed convolution, for speed and simplicity), and run a small 1x1 "lateral" convolution on the high-resolution map purely to make its channel count match the low-resolution map's — then add the two together.

Implement `nearest_upsample_2x(x)` and `fpn_merge(higher_res, lower_res, lateral_kernel)` against that reasoning.

### Constraints

- `nearest_upsample_2x(x)`: `x` shape `(C, H, W)` → returns shape `(C, 2H, 2W)`, each input pixel replicated into a 2x2 output block.
- `fpn_merge(higher_res, lower_res, lateral_kernel)`: `higher_res` shape `(C_high, 2H, 2W)`, `lower_res` shape `(C_low, H, W)` — exactly half `higher_res`'s spatial size — `lateral_kernel` shape `(C_low, C_high, 1, 1)`.
- Returns shape `(C_low, 2H, 2W)`.
- None of the inputs are modified in place.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`x.repeat(2, axis=1).repeat(2, axis=2)` repeats every row twice, then every column twice — together that turns each single pixel into a 2x2 block of identical copies (nearest-neighbor upsampling).

</details>

<details>
<summary>Hint 2</summary>

`pointwise_conv(higher_res, lateral_kernel)` projects `higher_res` from `C_high` to `C_low` channels (the "lateral connection") — add that to `nearest_upsample_2x(lower_res)`, which is already `C_low` channels and now the right spatial size too.

</details>

## Theory

### The simple version

Imagine two witnesses to the same event: one stood close up and remembers exact, fine details but has no idea what the bigger picture means; the other watched from far away and understands the overall situation well but is fuzzy on specifics. A feature pyramid's merge step is like having the far-away witness's understanding "broadcast" back down to the close-up witness's level of detail — the close-up witness's fine-grained view gets combined, position by position, with the big-picture understanding, so nothing detailed is lost and nothing high-level is missing.

### The formula

```text
lateral    = pointwise_conv(higher_res, lateral_kernel)   # (C_high, 2H, 2W) -> (C_low, 2H, 2W)
upsampled  = nearest_upsample_2x(lower_res)                # (C_low, H, W) -> (C_low, 2H, 2W)
merged     = lateral + upsampled
```

### How PyTorch actually implements this

`torch.nn.functional.interpolate(x, scale_factor=2, mode='nearest')` is the real nearest-neighbor upsample this exercise's `nearest_upsample_2x` reimplements by hand. Real FPN implementations (as used in Faster R-CNN, RetinaNet, and most modern detectors) build a whole pyramid this way, top-down: starting from the coarsest feature map, repeatedly merge it into the next-finer one using exactly this lateral-conv-plus-upsample-plus-add pattern, then run a small 3x3 conv on each merged result to smooth out the "checkerboard" artifacts nearest-neighbor upsampling can introduce — that smoothing step is left out here to keep this exercise to the single core merge operation.

## Explanation

`x.repeat(2, axis=1)` duplicates every row along the height axis, and chaining `.repeat(2, axis=2)` then duplicates every column along the width axis — applying both turns a single pixel at `(i, j)` into an identical 2x2 block at `(2i, 2j)`, `(2i, 2j+1)`, `(2i+1, 2j)`, `(2i+1, 2j+1)` in the output, which is exactly what "nearest-neighbor" upsampling means: every output pixel simply copies its nearest input pixel's value. `pointwise_conv(higher_res, lateral_kernel)` (from `04-modern-cnn-concepts/03-1x1-convolution`) does no spatial mixing at all, purely remapping `higher_res`'s channel count from `C_high` to `C_low` so the shapes line up for addition — this is the "lateral connection," carrying the high-resolution map's spatial detail forward without altering it spatially. Adding `lateral + upsampled` combines the two: every spatial position now holds both the fine-grained (lateral) and coarse-but-semantic (upsampled) information for that location, fused into one feature map at the higher resolution.
