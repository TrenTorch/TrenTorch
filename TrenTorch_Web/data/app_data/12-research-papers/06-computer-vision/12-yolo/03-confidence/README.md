---
name: research-yolo-confidence
title: 'YOLO: The Confidence Score'
tags: [research-papers, computer-vision, detection, object-detection]
difficulty: Beginner
---

## Statement

### The problem, from first principles

YOLO's confidence for a box is the probability that an object is there times how well the box fits it. A box that is well placed but empty scores low, and so does a box on an object it misses.

### From theory to code

Implement `confidence(obj, iou_val)`, returning the product of the object probability and the IoU.

### Constraints

- Both inputs are between zero and one.

### Hints

<details>
<summary>Hint 1</summary>

Multiply the two numbers.

</details>

## Theory

### The simple version

The product rewards boxes that both contain an object and align with it. Non-maximum suppression then uses these scores to choose among overlapping boxes.

### The formula

$$C = P(\text{object}) \cdot \operatorname{IoU}(\text{pred}, \text{truth})$$

### How NumPy/PyTorch actually implements this

YOLO post-processing multiplies class probability by this confidence before thresholding.

## Explanation

At training time the target confidence is the IoU itself, so the score is calibrated to localization quality.
