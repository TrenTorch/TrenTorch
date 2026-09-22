---
name: potd-pin-image-downsample-maxpool
title: 'PIN IMAGE DOWNSAMPLE'
tags: [computer-vision]
difficulty: Beginner
---

## Statement

**Difficulty:** Easy
**Tags:** Computer Vision

---

### Story

Pinterest downsamples every pin image before it reaches the visual-search backbone. This max-pool
layer is the very first operation in that backbone, run on millions of images a day.

---

### The Math

2D max pooling with kernel size `k`, stride `s`, no padding: output size
`floor((H - k) / s) + 1` per dimension, each output cell is the max over its receptive field.

### Input Format

```
H W k s
p_1,1 ... p_1,W
...
p_H,1 ... p_H,W
```

### Output Format

Pooled matrix, row by row, matching the input's own numeric type (integer values stay integer,
otherwise 6-decimal floats).

### Constraints

- `1 <= H, W <= 512`, `1 <= k <= min(H, W)`, `1 <= s <= k`
- Time limit: 1.0 second.

---

### Example

**Input**

```
4 4 2 2
1 3 2 4
5 6 7 8
9 1 2 3
4 5 6 0
```

**Output**

```
6 8
9 6
```

## Theory

### The simple version

Max pooling slides a small window over a grid and keeps only the largest value in each window. Sliding the window by a stride different from its size just changes how much the windows overlap or skip.

### Stride and kernel are not the same number here

Unlike a simple non-overlapping pool (stride equal to kernel), this problem allows stride and kernel
to differ. `s > k` (windows with gaps between them, some pixels never touched by any window) and
`s < k` (overlapping windows) are both valid and must be handled by actually stepping by `s`, not by
assuming windows tile the grid.

### No padding, drop the remainder

There is no padding in this problem. When `k` and `s` do not evenly divide `H` or `W`, the trailing
rows or columns that do not fill a complete window are simply dropped rather than padded, exactly
matching a standard `MaxPool2d` with `ceil_mode=False`. The output-size formula
`floor((H - k) / s) + 1` already accounts for this: it is not an approximation to correct for
afterward.

### `k = 1` degenerates to plain downsampling

With `k = 1`, pooling is a no-op on each individual pixel; the operation still shrinks the grid, but
purely through the stride, picking every `s`-th pixel rather than through any actual maximum over
multiple values.

## Explanation

`max_pool_strided` computes the output height and width from the formula, then for each output cell
`(i, j)` takes the max of the window whose top-left corner is at row `i * s`, column `j * s`,
spanning `k` rows and `k` columns. Because the window's start position is `i * s` rather than `i * k`,
overlapping windows (`s < k`) and gapped windows (`s > k`) fall out of the same indexing without a
separate case for either, and any trailing partial window past the last full step is never visited,
since the loop only runs for `out_h` and `out_w` steps, exactly the count the drop-the-remainder
formula gives.
