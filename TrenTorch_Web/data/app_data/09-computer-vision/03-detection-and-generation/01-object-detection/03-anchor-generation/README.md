---
name: vision-anchor-generation
title: Anchor Box Generation
tags: [computer-vision, object-detection, anchors]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Predicting a box from scratch is hard for a network. Anchor-based detectors make it easier by laying down a dense grid of **anchor boxes**, fixed reference rectangles of several sizes and shapes at every position, and asking the network only to adjust each one. A feature map with `fh x fw` cells, whose stride is the number of image pixels per cell, gets anchors centred at each cell's centre. At every location there is one anchor per combination of **scale** (the square root of the box area) and **aspect ratio** (height divided by width). Each anchor keeps the area `scale^2` while its shape changes with the ratio.

### From theory to code

Implement `generate_anchors`.

### Constraints

- `generate_anchors(fh, fw, stride, scales, ratios)` returns an array of shape `(fh * fw * len(scales) * len(ratios), 4)` of boxes `(x1, y1, x2, y2)`.
- Cell `(i, j)` has centre `cy = (i + 0.5) * stride`, `cx = (j + 0.5) * stride`. For a scale `s` and ratio `r = h / w`, the anchor has `w = s / sqrt(r)` and `h = s * sqrt(r)`, so `w * h = s**2`.
- Order: cells row-major (`i` outer, `j` inner), then for each cell `scales` outer and `ratios` inner.
- The box is `(cx - w/2, cy - h/2, cx + w/2, cy + h/2)`.

### Hints

<details>
<summary>Hint 1</summary>

Compute the `(len(scales) * len(ratios), 2)` array of widths and heights once, then combine it with the grid of centres by broadcasting.

</details>

<details>
<summary>Hint 2</summary>

A ratio of 1 gives a square, a ratio above 1 gives a tall box.

</details>

## Theory

### The simple version

Casting a net of fishing nets: at every point on the sea you drop a few differently shaped nets, and the network only has to say which net caught a fish and how to adjust it.

### The formula

$$
w = \frac{s}{\sqrt r},\quad h = s\sqrt r,\quad (c_x, c_y) = \big((j + \tfrac12)\,\text{stride},\; (i + \tfrac12)\,\text{stride}\big)
$$

so every anchor at a given scale has the same area $s^2$ regardless of its ratio, and the number of anchors is $f_h f_w |S||R|$.

### How this is done in practice

Faster R-CNN used 3 scales and 3 ratios per location, RetinaNet and SSD use per-level scales on feature pyramids. Anchor-free detectors (FCOS, CenterNet) drop the idea and predict from cell centres directly, which removes the hand-tuned scales and ratios.

## Explanation

Broadcasting a base set of widths and heights against a grid of centres yields every anchor with no loops. The tests check count, area, aspect ratio and ordering, the properties that detection code relies on.
