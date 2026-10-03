---
name: vision-bilinear-resize
title: Bilinear Interpolation
tags: [computer-vision, interpolation, resize]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

To resize an image you must decide what value each output pixel should have, but the output pixel generally maps to a _fractional_ location in the input. **Bilinear interpolation** estimates the value there from the four surrounding input pixels, weighting each by how close it is: first interpolate horizontally along the two rows, then vertically between those results. A subtle detail decides whether your resize matches the libraries: the convention for where a pixel's coordinate sits. Treating a pixel as a unit square whose **center** is at `index + 0.5` gives the mapping `src = (dst + 0.5) * (in_size / out_size) - 0.5`, which keeps the image centered when scaling.

### From theory to code

Implement `bilinear_resize`.

### Constraints

- `img` has shape `(H, W)`. `bilinear_resize(img, out_h, out_w)` returns shape `(out_h, out_w)`.
- For output pixel `(i, j)` the source coordinates are `y = (i + 0.5) * H / out_h - 0.5` and `x = (j + 0.5) * W / out_w - 0.5`, clipped to `[0, H - 1]` and `[0, W - 1]`.
- With `y0 = floor(y)`, `y1 = min(y0 + 1, H - 1)` and `wy = y - y0` (same for `x`), the value is the bilinear blend of the four neighbours with those weights.
- Do not modify the input.

### Hints

<details>
<summary>Hint 1</summary>

Compute the coordinate arrays once for rows and columns, then use `np.ix_`-style broadcasting (`y0[:, None]`, `x0[None, :]`) to gather the four neighbours.

</details>

<details>
<summary>Hint 2</summary>

Clipping before taking the floor makes the edges replicate rather than extrapolate.

</details>

## Theory

### The simple version

Resizing a mosaic: each new tile covers a spot between four old tiles, so its colour is a blend that leans toward whichever old tile is nearest.

### The formula

$$
f(y, x) = (1 - w_y)\big[(1 - w_x) I_{y_0 x_0} + w_x I_{y_0 x_1}\big] + w_y\big[(1 - w_x) I_{y_1 x_0} + w_x I_{y_1 x_1}\big]
$$

Interpolation is linear in the pixel values, so a constant image stays constant and a linear ramp stays a linear ramp.

### How this is done in practice

`torch.nn.functional.interpolate(mode='bilinear', align_corners=False)` and OpenCV's `cv2.resize` use this pixel-center convention. `align_corners=True` instead aligns the corner pixels exactly and gives slightly different values, a frequent source of mismatches when porting models between frameworks.

## Explanation

Everything is gather-and-blend with precomputed index and weight arrays. The hand-computed test (upsampling a 1x2 image) pins down the half-pixel convention.
