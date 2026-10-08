---
name: research-frcnn-nms
title: 'Faster R-CNN: Non-maximum Suppression'
tags: [research-papers, computer-vision, detection, object-detection]
difficulty: Advanced
---

## Statement

### The problem, from first principles

Detectors produce many overlapping boxes for the same object. Non-maximum suppression keeps the best-scoring box and removes any other box that overlaps it too much, leaving one detection per object.

### From theory to code

Implement `nms(boxes, scores, thr)`, returning the indices of the kept boxes in score order.

### Constraints

- Overlap is measured with IoU; suppress boxes with IoU above `thr`.

### Hints

<details>
<summary>Hint 1</summary>

Sort the indices by score. Walk through them, keeping each box that has IoU at most `thr` with every box already kept.

</details>

## Theory

### The simple version

The greedy pass guarantees that no two kept boxes overlap too much, while letting an unrelated object nearby survive.

### The formula

$$\text{keep } b_i \iff \operatorname{IoU}(b_i, b_j) \le \tau \;\;\forall\, b_j \text{ kept with higher score}$$

### How NumPy/PyTorch actually implements this

Torchvision's `nms` implements the same greedy algorithm on GPU for batches of boxes.

## Explanation

The greedy order is what makes NMS fast and predictable; the highest score always survives.
