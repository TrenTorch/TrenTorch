---
name: research-yolo-decode-xy
title: 'YOLO: Decoding the Box Centre'
tags: [research-papers, computer-vision, detection, object-detection]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

YOLO predicts a box centre relative to the cell that owns it. A sigmoid keeps the predicted offset between zero and one, so the centre cannot leave its cell, and the offset is converted back to image pixels.

### From theory to code

Implement `decode_xy(sx, sy, col, row, S, img)`, returning the box centre in pixels.

### Constraints

- Use a sigmoid on the raw offsets.

### Hints

<details>
<summary>Hint 1</summary>

Apply the sigmoid to each raw offset, add the cell index, then multiply by the cell size in pixels.

</details>

## Theory

### The simple version

Constraining the centre to its cell removes the ambiguity of which cell predicts an object, and the sigmoid keeps training numerically stable.

### The formula

$$x = \left(\text{col} + \sigma(s_x)\right)\frac{W}{S}, \qquad y = \left(\text{row} + \sigma(s_y)\right)\frac{H}{S}$$

### How NumPy/PyTorch actually implements this

YOLO decoders apply sigmoid to the centre outputs and scale by the grid stride, as in this formula.

## Explanation

A raw output of zero puts the centre at the middle of its cell, which the first test checks.
