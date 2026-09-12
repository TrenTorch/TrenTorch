---
name: vision-history-dilated-conv
title: Dilated Convolution
tags: [computer-vision, cnn, history, receptive-field]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Growing a network's receptive field (how much of the input each output pixel "sees") the naive way costs something: bigger kernels mean more parameters, and stacking more layers means more depth and more downsampling (losing spatial resolution, which segmentation and dense-prediction tasks specifically can't afford to lose). Dilated ("atrous," from the French for "with holes") convolution grows the receptive field for free — same kernel, same parameter count — by spacing out where the kernel looks, skipping pixels between each tap instead of looking at a contiguous patch.

### From theory to code

Theory says: instead of a kernel scanning a contiguous `kH x kW` patch, spread its taps `dilation` pixels apart, so the same `kH x kW` set of weights now spans a `(kH-1)*dilation + 1` by `(kW-1)*dilation + 1` region of the input — the kernel's *effective* footprint grows even though its *parameter count* (`kH * kW`) doesn't.

Implement `dilated_conv2d(image, kernel, dilation=1)` against that reasoning.

### Constraints

- `image`: shape `(H, W)`.
- `kernel`: shape `(kH, kW)`.
- `dilation`: positive integer; `dilation=1` is an ordinary, non-dilated convolution.
- Output shape: `(H - eff_kH + 1, W - eff_kW + 1)`, where `eff_kH = (kH - 1) * dilation + 1` (same formula for `eff_kW`).
- `image` and `kernel` are never modified in place.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Compute `eff_kH = (kH - 1) * dilation + 1` and `eff_kW` the same way, once, before the main loop — these are the true spatial span the kernel now reaches, even though the kernel array itself is still only `kH x kW`.

</details>

<details>
<summary>Hint 2</summary>

For output position `(i, j)`, the slice `image[i : i+eff_kH : dilation, j : j+eff_kW : dilation]` — note the `dilation` step — picks out exactly the `kH x kW` pixels the spread-out kernel taps land on, ready to multiply elementwise against `kernel` and sum.

</details>

## Theory

### The simple version

Picture a person scanning a page for information by reading every single word (a plain, dilation-1 convolution) versus someone skimming by reading every third word (dilation-3): the skimmer covers three times the page in the same number of words read, at the cost of missing whatever falls between the words they picked. A dilated convolution makes the same trade for images — its kernel "reads" a much larger area with the same number of weights, at the cost of literally never looking at most of the pixels inside that larger area (only the ones landing exactly on a dilated tap).

### The formula

```text
eff_kH = (kH - 1) * dilation + 1        # kernel's effective span, same formula for eff_kW
for each output position (i, j):
    patch = image[i : i+eff_kH : dilation, j : j+eff_kW : dilation]   # strided slice
    output[i, j] = sum(patch * kernel)
```

### How PyTorch actually implements this

`torch.nn.Conv2d(..., dilation=d)` and `torch.nn.functional.conv2d(..., dilation=d)` support this natively as a first-class argument, identical in spirit to this exercise's `dilation` parameter. Dilated convolutions are the core building block of DeepLab and other semantic segmentation architectures, which specifically need a large receptive field (to understand object-level context) WITHOUT downsampling the feature map's resolution (since the final output needs a label for every original pixel) — stacking dilated convolutions with increasing dilation rates (1, 2, 4, 8, ...) is a standard way to grow receptive field exponentially while keeping spatial resolution and parameter count both fixed.

## Explanation

`eff_kH = (kH - 1) * dilation + 1` computes the true pixel-to-pixel span of the spread-out kernel: at `dilation=1` this reduces to `kH` exactly (an ordinary convolution), and at `dilation=2` a `3x3` kernel's 3 taps per row now span 5 pixels (tap, gap, tap, gap, tap) instead of 3. The strided slice `image[i : i+eff_kH : dilation, ...]` is what actually implements "skip the gaps" — a step of `dilation` in a NumPy slice visits every `dilation`-th index starting from `i`, which lands exactly on the `kH` positions the dilated kernel's taps are meant to read, and nowhere else; multiplying that strided patch elementwise against the ordinary, un-strided `kernel` array then works because both now have the same `(kH, kW)` shape, even though the patch's pixels came from a much wider span of the original image.
