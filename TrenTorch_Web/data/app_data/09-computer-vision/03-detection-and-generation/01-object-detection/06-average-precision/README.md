---
name: vision-average-precision
title: Average Precision
tags: [computer-vision, object-detection, metrics]
difficulty: Advanced
---

## Statement

### The problem, from first principles

How good is a detector? Accuracy does not apply because a detector outputs a _ranked list_ of boxes with scores, and the number of objects found depends on where you cut the list. **Average precision** (AP) summarizes the whole list. Sort the detections of one class by confidence. Walk down the list, marking each detection as a **true positive** (it matches a previously unmatched ground-truth box with IoU above a threshold) or a **false positive**. After each step compute precision (`TP / detections so far`) and recall (`TP / total ground truths`). Plotting precision against recall gives a zig-zag curve, and AP is the area under it after replacing each precision by the **best precision at any higher recall**, which removes the zig-zag. Averaging AP over classes gives mAP.

### From theory to code

Implement `average_precision`.

### Constraints

- `scores` is a length-`D` array of detection confidences, `is_tp` is a length-`D` boolean array saying whether each detection is a true positive (matching has already been done), and `n_gt` is the number of ground-truth boxes (`n_gt >= 1`).
- Sort by descending score (stable). Compute cumulative `tp` and `fp`, `recall = tp / n_gt` and `precision = tp / (tp + fp)`.
- Use the **all-point interpolation** of Pascal VOC 2010+: prepend `recall = 0` and `precision = 1`, append `recall = 1` and `precision = 0`, make precision monotone non-increasing from right to left (`precision[i] = max(precision[i], precision[i+1])`), and sum `(recall[i+1] - recall[i]) * precision[i+1]` over the points where recall changes.
- Return a float. With no detections, return `0.0`.

### Hints

<details>
<summary>Hint 1</summary>

`np.maximum.accumulate(precision[::-1])[::-1]` produces the monotone envelope.

</details>

<details>
<summary>Hint 2</summary>

`np.where(recall[1:] != recall[:-1])` selects the indices where the area is added.

</details>

## Theory

### The simple version

A librarian ranks books by how likely each is to match your query. AP rewards putting all the right books near the top and finding all of them; one bad book early hurts, one missing book hurts recall.

### The formula

$$
\text{AP} = \sum_{k} (r_{k+1} - r_k)\, p_{\text{interp}}(r_{k+1}), \qquad p_{\text{interp}}(r) = \max_{r' \ge r} p(r')
$$

mAP averages AP over classes, and COCO further averages over IoU thresholds from 0.5 to 0.95.

### How this is done in practice

`pycocotools` and `torchmetrics.detection.MeanAveragePrecision` implement the full pipeline including the box matching. COCO uses 101-point interpolation instead of all-point, which gives slightly different numbers, so papers always state the protocol.

## Explanation

Matching boxes to ground truth is separated out, so this function is the pure ranking metric. The tests verify the two extreme cases (perfect ranking gives 1, all false positives gives 0) and a worked example with a missed object.
