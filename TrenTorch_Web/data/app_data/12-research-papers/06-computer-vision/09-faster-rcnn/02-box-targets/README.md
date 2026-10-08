---
name: research-frcnn-box-targets
title: 'Faster R-CNN: Bounding Box Regression Targets'
tags: [research-papers, computer-vision, detection, object-detection]
difficulty: Advanced
---

## Statement

### The problem, from first principles

The region proposal network refines each anchor box by predicting four offsets: a centre shift scaled by the box size, and a log scale change for width and height. These are the targets the network regresses toward.

### From theory to code

Implement `box_targets(anchor, gt)`, returning `(tx, ty, tw, th)` from the anchor to the ground truth.

### Constraints

- Widths and heights are positive.

### Hints

<details>
<summary>Hint 1</summary>

Convert both boxes to center and size. Take center differences divided by the anchor size, and log ratios of sizes.

</details>

## Theory

### The simple version

Normalizing by the anchor size makes the targets scale-invariant. Logs make width and height changes symmetric for growing and shrinking.

### The formula

$$t_x = \frac{x - x_a}{w_a},\; t_y = \frac{y - y_a}{h_a},\; t_w = \log\frac{w}{w_a},\; t_h = \log\frac{h}{h_a}$$

### How NumPy/PyTorch actually implements this

Detection frameworks encode targets with this exact parameterization in their box coders.

## Explanation

The regression loss in the paper is applied to these four values, and inference inverts the same formulas.
