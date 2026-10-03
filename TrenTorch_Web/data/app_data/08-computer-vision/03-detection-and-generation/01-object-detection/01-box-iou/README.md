---
name: vision-box-iou
title: Intersection over Union
tags: [computer-vision, object-detection, metrics]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Object detectors output boxes, and almost everything about them depends on one question: how much do two boxes overlap? **Intersection over union** answers it with a number between 0 and 1. The intersection is the overlapping rectangle (whose width and height must be clamped at zero when the boxes do not touch), and the union is the sum of both areas minus the intersection so it is not counted twice. IoU is used to decide whether a prediction matches a ground-truth box, to suppress duplicate detections and to assign training targets to anchors, so it is computed between _every pair_ of two sets of boxes at once, which makes broadcasting the heart of this exercise.

### From theory to code

Implement `box_iou`.

### Constraints

- Boxes are `(x1, y1, x2, y2)` with `x2 >= x1` and `y2 >= y1`. `a` has shape `(N, 4)` and `b` has shape `(M, 4)`.
- `box_iou(a, b)` returns the `(N, M)` matrix of pairwise IoUs. Intersection width and height are clamped at 0.
- If the union area is 0 (both boxes degenerate), the IoU is `0.0`.
- Do not modify the inputs.

### Hints

<details>
<summary>Hint 1</summary>

Broadcast `a[:, None, :]` against `b[None, :, :]` to get all pairs at once.

</details>

<details>
<summary>Hint 2</summary>

Intersection corners: `max` of the top-left corners and `min` of the bottom-right corners.

</details>

## Theory

### The simple version

Two sheets of paper on a table: the overlapping region divided by the total area they cover together. Sliding them apart takes the fraction from 1 down to 0.

### The formula

$$
\text{IoU}(A, B) = \frac{|A \cap B|}{|A \cup B|} = \frac{|A \cap B|}{|A| + |B| - |A \cap B|}, \qquad
|A \cap B| = \max(0, x_2^\cap - x_1^\cap)\cdot\max(0, y_2^\cap - y_1^\cap)
$$

### How this is done in practice

`torchvision.ops.box_iou` is exactly this function. Variants add a penalty for non-overlapping boxes (GIoU, DIoU, CIoU), which gives a useful gradient even when IoU is zero, and are used as regression losses.

## Explanation

Two broadcasts give the intersection corners, a clamp handles disjoint boxes and a final division produces the matrix. The tests include touching boxes, nested boxes and degenerate boxes.
