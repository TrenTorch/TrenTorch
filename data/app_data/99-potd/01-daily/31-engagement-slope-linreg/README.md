---
name: potd-engagement-slope-linreg
title: 'ENGAGEMENT SLOPE'
tags: [regression]
difficulty: Beginner
---

## Statement

**Difficulty:** Easy
**Tags:** Regression

---

### Story

A lightweight linear model relating post length to engagement is the very first thing a new
content-ranking hire implements at Meta: a rite of passage, and a correctness bar every later
ranking model gets compared against.

---

### The Math

```
w = sum((x_i - mean_x) * (y_i - mean_y)) / sum((x_i - mean_x)^2)
b = mean_y - w * mean_x
```

### Input Format

```
n
x_1 y_1
...
x_n y_n
```

### Output Format

`w b`, 6 decimals.

### Constraints

- `2 <= n <= 10^5`
- Time limit: 1.0 second.

---

### Example

**Input**

```
5
1 50
2 55
3 65
4 70
5 80
```

**Output**

```
7.500000 41.500000
```

## Theory

### The simple version

Simple linear regression finds the one straight line that best follows a scatter of points, by minimizing how far off the line's predictions are on average.

### All `x_i` identical

If every `x_i` is the same value, `sum((x_i - mean_x)^2)` is exactly `0` and `w`'s formula divides
by zero. The convention here: `w = 0.000000`, `b = mean_y`, a flat line through the average `y`.
This must be a stated convention rather than left to whatever a particular language's
division-by-zero behavior happens to produce, since different languages disagree on that.

### Noiseless and noisy data get the same treatment

The formula does not special-case a perfect fit; it always computes the least-squares-optimal line,
whether the points happen to lie exactly on a line (as in the example) or are scattered around one.

### One pass for both sums

`mean_x` and `mean_y` need a first pass; the covariance and variance sums need `x_i - mean_x` and
`y_i - mean_y`, which need the means already computed. Two passes total (means, then the two sums),
never `O(n^2)`.

## Explanation

`fit_line` computes `mean_x` and `mean_y` first, then in a second pass accumulates
`sum((x - mean_x) * (y - mean_y))` for the numerator and `sum((x - mean_x)**2)` for the denominator.
If the denominator is exactly `0`, it returns `(0.0, mean_y)` directly instead of dividing;
otherwise `w = numerator / denominator` and `b = mean_y - w * mean_x` follow the formula exactly, so
noiseless and noisy inputs both flow through the same two-pass computation.
