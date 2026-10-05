---
name: vision-box-encode-decode
title: Box Encoding & Decoding
tags: [computer-vision, object-detection, regression]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

The network does not output raw coordinates. For each anchor it predicts four numbers that describe how to **transform the anchor into the target box**. The centre offsets `dx` and `dy` are expressed as a fraction of the anchor's width and height, which makes them scale-free: moving by 10% of the box means the same for a small and a large anchor. The size changes `dw` and `dh` are log-ratios, so that doubling the width is `+ln 2` and halving is `-ln 2`, symmetric around zero and always positive when exponentiated. **Encoding** turns a ground-truth box into these four numbers for training, and **decoding** applies the predicted numbers to an anchor to get a box back.

### From theory to code

Implement `encode_boxes` and `decode_boxes`.

### Constraints

- Boxes are `(x1, y1, x2, y2)`. For an anchor with centre `(ax, ay)` and size `(aw, ah)` and a ground-truth box with centre `(gx, gy)` and size `(gw, gh)`: `dx = (gx - ax) / aw`, `dy = (gy - ay) / ah`, `dw = log(gw / aw)`, `dh = log(gh / ah)`.
- `encode_boxes(gt, anchors)` takes two `(N, 4)` arrays and returns `(N, 4)` deltas `[dx, dy, dw, dh]`.
- `decode_boxes(deltas, anchors)` is the exact inverse and returns `(N, 4)` boxes in `(x1, y1, x2, y2)`.
- Do not modify the inputs.

### Hints

<details>
<summary>Hint 1</summary>

Convert corners to centre-size form first; do the maths there; convert back at the end.

</details>

<details>
<summary>Hint 2</summary>

`decode(encode(gt, a), a)` must reproduce `gt`.

</details>

## Theory

### The simple version

Instead of saying where a house is by its map coordinates, you say "from the corner shop, go 10% of a street's width east and make it twice as tall". Directions relative to a reference are easier to learn than absolute ones.

### The formula

$$
d_x = \frac{g_x - a_x}{a_w},\quad d_y = \frac{g_y - a_y}{a_h},\quad d_w = \ln\frac{g_w}{a_w},\quad d_h = \ln\frac{g_h}{a_h}
$$

Inverting gives $g_x = a_x + a_w d_x$, $g_w = a_w e^{d_w}$, and similarly for $y$ and $h$.

### How this is done in practice

This is the parametrization from R-CNN, used in Faster R-CNN, SSD and RetinaNet, usually with fixed scaling constants (weights such as `(10, 10, 5, 5)`) that balance the targets. Predicted `dw` is clamped before `exp` in practice to avoid overflow.

## Explanation

The only trick is the centre-size conversion, repeated in both directions. A round trip test is the best check: if decoding the encoded targets returns the original boxes, the two functions agree.
