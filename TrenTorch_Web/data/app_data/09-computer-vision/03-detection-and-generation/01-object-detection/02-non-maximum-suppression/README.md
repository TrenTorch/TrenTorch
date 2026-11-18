---
name: vision-non-maximum-suppression
title: Non-Maximum Suppression
tags: [computer-vision, object-detection, post-processing]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

A detector fires many overlapping boxes around the same object, each with a confidence score. Reporting all of them would count one cat five times. **Non-maximum suppression** (NMS) keeps the best and discards its near-duplicates: sort the boxes by score; take the highest-scoring box and keep it; remove every remaining box whose IoU with it exceeds a threshold; repeat with what is left. A box far from the kept one survives and may be kept later, so two different cats are both detected. The threshold is a trade-off: too low suppresses neighbouring objects, too high leaves duplicates.

### From theory to code

Implement `nms`.

### Constraints

- `boxes` has shape `(N, 4)` as `(x1, y1, x2, y2)`, `scores` has shape `(N,)` and `iou_thresh` is a float.
- Process boxes in order of **descending score** (ties by lower index first). Keep a box unless a previously kept box has IoU **strictly greater** than `iou_thresh` with it.
- Return the indices of the kept boxes (into the original arrays) as a list in the order they were kept.
- Include your own IoU computation. Do not modify the inputs.

### Hints

<details>
<summary>Hint 1</summary>

Keep a boolean `suppressed` array and iterate over `np.argsort(-scores, kind='stable')`.

</details>

<details>
<summary>Hint 2</summary>

When a box is kept, mark every other box with IoU above the threshold as suppressed.

</details>

## Theory

### The simple version

Of ten people pointing at the same bird, keep the most confident witness and ignore the rest, but keep a second witness who points at a different bird.

### The formula

$$
\text{keep } i \iff \forall\, j \in \text{kept},\; \text{IoU}(b_i, b_j) \le \tau
$$

in descending-score order. The greedy procedure is quadratic in the number of boxes in the worst case.

### How this is done in practice

`torchvision.ops.nms` and `batched_nms` (per class) are the production versions. Soft-NMS decays scores instead of deleting boxes, and transformer detectors such as DETR remove the need for NMS entirely by predicting a set with one-to-one matching.

## Explanation

The sorted greedy loop is the whole algorithm. The strict inequality at the threshold is a detail that matters for reproducing library output exactly, and is checked by a test.
