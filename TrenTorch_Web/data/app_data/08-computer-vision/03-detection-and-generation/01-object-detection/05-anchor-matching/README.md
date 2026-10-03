---
name: vision-anchor-matching
title: Anchor Matching
tags: [computer-vision, object-detection, training-targets]
difficulty: Advanced
---

## Statement

### The problem, from first principles

Training an anchor-based detector requires deciding, for every anchor, what it is _supposed_ to detect. The standard rule uses IoU with the ground-truth boxes. An anchor whose best IoU is at least `pos_thresh` is a **positive** and is assigned the ground-truth box it overlaps most. An anchor whose best IoU is below `neg_thresh` is a **negative** (background). Anchors in between are **ignored** because they are ambiguous and would only add noise to the loss. One extra rule rescues small objects: every ground-truth box also claims its single best-matching anchor as a positive, even if the IoU is below the threshold, so no object is left without a training signal.

### From theory to code

Implement `match_anchors`.

### Constraints

- `anchors` has shape `(A, 4)` and `gt_boxes` has shape `(G, 4)`, both `(x1, y1, x2, y2)`. Compute the `(A, G)` IoU matrix yourself.
- Return an integer array `matches` of length `A`: the index of the matched ground-truth box for positives, `-1` for negatives and `-2` for ignored anchors.
- Rules in order: (1) for each anchor take its best ground-truth by IoU (lowest index on ties); `>= pos_thresh` marks it positive, `< neg_thresh` negative, otherwise ignore. (2) For each ground-truth box, take the anchor with the highest IoU for it (lowest index on ties); if that IoU is greater than 0 force the anchor to be positive with that ground truth (this overrides rule 1, and later ground truths override earlier ones).
- If `G == 0`, every anchor is negative.

### Hints

<details>
<summary>Hint 1</summary>

Positives' targets are then encoded with the box encoding from the previous question.

</details>

<details>
<summary>Hint 2</summary>

Rule 2 is applied after rule 1 so it can promote an ignored or negative anchor.

</details>

## Theory

### The simple version

Assigning workers to tasks: a worker already close enough to a task takes it, a worker nowhere near anything is dismissed, and a task nobody is close to still gets the nearest worker so it is not forgotten.

### The formula

$$
m_a = \begin{cases} \arg\max_g \text{IoU}(a, g) & \max_g \text{IoU} \ge \tau_+\\ -1 & \max_g \text{IoU} < \tau_-\\ -2 & \text{otherwise}\end{cases}
\qquad\text{then}\quad m_{\arg\max_a \text{IoU}(a, g)} \leftarrow g
$$

### How this is done in practice

Faster R-CNN uses `(0.7, 0.3)` for its region proposal network, RetinaNet uses `(0.5, 0.4)`. SSD adds hard-negative mining to rebalance the many negatives. Modern detectors replace the fixed thresholds with dynamic assignment (ATSS, SimOTA) or one-to-one Hungarian matching.

## Explanation

The IoU matrix is reduced twice: along the ground-truth axis for the threshold rule and along the anchor axis for the forced matches. The tests exercise each rule separately, including the rescue of a small object.
