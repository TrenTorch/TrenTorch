---
name: vision-conv-padding
title: 'Padding: Same vs. Valid'
tags: [computer-vision, convolutions, padding]
difficulty: Beginner
---

## Statement

### The problem, from first principles

`01-single-filter-conv2d`'s output is always smaller than its input — a kernel can't hang off the edge, so every convolution shrinks the image a little. Stack enough convolutional layers and an image eventually shrinks to nothing, which is rarely what you want for a deep network's middle layers.

The fix is to give the kernel somewhere to go at the edges: surround the image with a border of zeros first, wide enough that the kernel can center itself on every original pixel, including the ones right at the edge. Do that and the output comes out the same size as the input went in.

### From theory to code

Theory gives two modes: `"valid"` is exactly what `01-single-filter-conv2d` already does — no border, output shrinks. `"same"` adds a zero border of the right width first, then runs the identical convolution.

Implement `conv2d_with_padding(image, kernel, padding="valid")` against that reasoning, reusing `01-single-filter-conv2d`'s `conv2d_single_filter` rather than reimplementing the sliding-window logic.

### Constraints

- `image`: shape `(H, W)`. `kernel`: shape `(kH, kW)`, both dimensions odd.
- `padding="valid"`: no padding, output shape `(H - kH + 1, W - kW + 1)`.
- `padding="same"`: zero-pad by `(kH-1)//2` and `(kW-1)//2` on each side per axis, output shape exactly `(H, W)`.
- Any other `padding` value raises `ValueError`.
- `image` and `kernel` are never modified in place.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`"valid"` needs no new logic at all — it's a direct call to `conv2d_single_filter`.

</details>

<details>
<summary>Hint 2</summary>

`np.pad(image, ((pad_h, pad_h), (pad_w, pad_w)))` adds a zero border of `pad_h` rows and `pad_w` columns on every side. Compute `pad_h`, `pad_w` from the kernel's shape, then convolve the padded image exactly as in `"valid"`.

</details>

## Theory

### The simple version

Imagine laying a photo on a larger blank white sheet before scanning it with a stencil — now the stencil can center itself right on the photo's own edge pixels without ever falling off the sheet. The scan produces one result per pixel of the ORIGINAL photo, edges included, instead of skipping every position the stencil couldn't fully fit over.

### The formula

```text
pad_h = (kH - 1) // 2
pad_w = (kW - 1) // 2
padded_image = zero-pad image by pad_h rows and pad_w columns on every side
output = conv2d_single_filter(padded_image, kernel)   # now shape (H, W)
```

This only comes out exactly `(H, W)` for odd kernel sizes — an even kernel can't be centered symmetrically on a single pixel, which is exactly why odd kernel sizes (`1x1`, `3x3`, `5x5`, ...) are the overwhelming convention in real CNN architectures.

### How PyTorch actually implements this

`torch.nn.functional.conv2d(image, kernel, padding='same')` and `padding='valid'` implement exactly these two modes — `'valid'` is the library's own default when `padding` is left unspecified. Real architectures (ResNet, VGG, and nearly everything since) use `'same'`-style padding throughout their convolutional layers specifically so stacking many layers doesn't erode the spatial size down to nothing before the network is done extracting features.

## Explanation

`"valid"` delegates directly to `01-single-filter-conv2d`'s `conv2d_single_filter` — there's no new computation, just the existing sliding-window logic reused unchanged. `"same"` computes `pad_h = (kH-1)//2` and `pad_w = (kW-1)//2` from the kernel's own shape, then `np.pad` surrounds `image` with that many zero rows/columns on every side before handing the padded array to the same `conv2d_single_filter` call. Because the padded image is now `(H + 2*pad_h, W + 2*pad_w)`, a valid convolution over it produces exactly `(H + 2*pad_h - kH + 1, ...) = (H, W)` when `pad_h = (kH-1)//2` — the padding width is chosen precisely to make that arithmetic work out to the original size.
