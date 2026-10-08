---
name: research-frcnn-iou
title: 'Faster R-CNN: Intersection over Union'
tags: [research-papers, computer-vision, detection, object-detection]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Faster R-CNN (Ren et al., 2015) proposes regions, then classifies and refines them. Intersection over union measures how well a proposal overlaps a ground-truth box, and it drives both training labels and the removal of duplicate detections.

### From theory to code

Implement `iou(a, b)`, the ratio of the overlap area to the combined area of two boxes.

### Constraints

- Boxes are `[x1, y1, x2, y2]`.

### Hints

<details>
<summary>Hint 1</summary>

Find the intersection rectangle; if it is empty the overlap is zero. Divide the intersection area by the sum of the two areas minus the intersection.

</details>

## Theory

### The simple version

IoU is scale-invariant, so the same threshold works for large and small objects. The paper labels a proposal positive when its IoU with a ground-truth box is high.

### The formula

$$\operatorname{IoU}(A,B) = \frac{|A \cap B|}{|A| + |B| - |A \cap B|}$$

### How NumPy/PyTorch actually implements this

Detection libraries use this IoU in their matching and non-maximum suppression, often vectorized over many boxes.

## Explanation

The max and min on coordinates give the intersection rectangle; the clamp to zero handles disjoint boxes.
