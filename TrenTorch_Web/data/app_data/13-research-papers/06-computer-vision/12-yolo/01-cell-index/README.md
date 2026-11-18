---
name: research-yolo-cell-index
title: 'YOLO: Assigning an Object to a Grid Cell'
tags: [research-papers, computer-vision, detection, object-detection]
difficulty: Beginner
---

## Statement

### The problem, from first principles

YOLO (Redmon et al., 2016) divides the image into an S by S grid. The cell that contains an object's centre is responsible for predicting it, so each object has exactly one responsible cell.

### From theory to code

Implement `cell_index(x, y, img, S)`, returning the grid cell that contains the object centre.

### Constraints

- Coordinates on the far edge belong to the last cell.

### Hints

<details>
<summary>Hint 1</summary>

Scale the coordinate to grid units, floor it, and clamp to `S - 1`.

</details>

## Theory

### The simple version

Responsibility by centre makes the training target unambiguous: one cell predicts each object, and the other cells learn that they have no object to report.

### The formula

$$\text{col} = \min\!\left(\left\lfloor\frac{x}{W}S\right\rfloor, S-1\right),\qquad \text{row} = \min\!\left(\left\lfloor\frac{y}{H}S\right\rfloor, S-1\right)$$

### How NumPy/PyTorch actually implements this

YOLO target builders compute this cell index for each ground-truth box before assigning it to the grid.

## Explanation

The clamp handles centres at exactly the image edge, which would otherwise index past the grid.
