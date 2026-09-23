---
name: potd-thumbnail-normalize
title: 'THUMBNAIL NORMALIZE'
tags: [computer-vision, data-processing]
difficulty: Beginner
---

## Statement

**Difficulty:** Easy
**Tags:** Computer Vision, Data Processing

---

### Story

Netflix normalizes every uploaded artwork candidate before it reaches the thumbnail-ranking CNN.
Get the normalization wrong and the model silently sees out-of-distribution inputs with no error
thrown anywhere.

---

### The Math

```
x' = (x - mu) / sigma
```

where `mu` and `sigma` are the mean and **population** standard deviation of the pixel values in
the given image.

### Input Format

```
H W
p_1,1 ... p_1,W
...
p_H,1 ... p_H,W
```

### Output Format

First line: `mu` and `sigma`. Then the `H x W` normalized matrix, row by row, all to 6 decimals.

### Constraints

- `1 <= H, W <= 512`
- Time limit: 1.0 second.

---

### Example

**Input**

```
2 2
100 150
200 250
```

**Output**

```
175.000000 55.901699
-1.341641 -0.447214
0.447214 1.341641
```

## Theory

### The simple version

Z-score normalization recenters a set of numbers around 0 and rescales them so a typical distance from the center is 1. It turns "this pixel is 175" into "this pixel is about average" or "this pixel is unusually bright."

### Population, not sample

This is the population standard deviation: divide the sum of squared deviations by `n`, the pixel
count, not `n - 1`. Many statistics libraries default to the sample convention (`n - 1`), and
switching without noticing produces a value close enough to look plausible while being wrong on
every non-trivial case.

### A constant image has no spread

If every pixel in the image is the same value, `sigma = 0` and the formula divides by zero. The
defined convention here: output an all-zero normalized image rather than `NaN` or a crash. A single
pixel (`H = W = 1`) is the same case: `sigma = 0` trivially.

### Wide dynamic range

Sensor data at 16-bit range (`0` to `65535`) makes the intermediate `(x - mu)^2` values large. Using
double-precision floats throughout (NumPy's default) keeps the variance computation accurate at
that range without a special code path.

## Explanation

`normalize_image` computes `mu = matrix.mean()` and the population `sigma = matrix.std()` (NumPy's
`.std()` defaults to `ddof=0`, the population convention, already matching what this problem asks
for). If `sigma` is exactly `0`, it returns an all-zero array the same shape as the input instead of
dividing; otherwise it returns `(matrix - mu) / sigma` directly, which NumPy broadcasts over the
whole image in one vectorized pass.
