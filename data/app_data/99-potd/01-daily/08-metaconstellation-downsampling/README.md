---
name: vision-pool-metaconstellation-downsampling
title: 'PALANTIR EDGE AI: META-CONSTELLATION DOWNSAMPLING'
tags: [computer-vision, pooling, array-manipulation, edge-inference]
difficulty: Beginner
---

## Statement

**Difficulty:** Easy
**Tags:** Computer Vision, Max Pooling, Array Manipulation, Edge Inference

---

### Story

Palantir's MetaConstellation software integrates with satellite constellations to run
object-detection micro-models on-orbit using Edge AI. High-resolution multispectral imagery is
massive. To reduce the bandwidth needed to downlink it to tactical ground stations, the onboard
micro-models downsample the imagery spatially, compressing the data while keeping the critical
intelligence.

Your task is the forward pass of a 2D max pooling layer, the same operation as the Max Pooling
question in the Vision track, written from scratch. You are given a single-channel feature map that
holds radar or thermal signatures of ships or buildings. By keeping the maximum response in each
local patch, you preserve the strongest signals (a hot engine, a metal hull) while shrinking the
image dimensions.

---

### The Math: Max Pooling

Given an `N x N` input matrix `X` and a pooling window of size `F`, with a stride equal to `F`
(the windows do not overlap), the output `Y` is an `M x M` matrix where `M = N / F`.

For every output position `(i, j)` with `0 <= i < M` and `0 <= j < M`, the value is the maximum of
the matching `F x F` patch of the input:

```
Y[i][j] = max( X[i*F + a][j*F + b] )   over all 0 <= a < F and 0 <= b < F
```

---

### Input Format

```
N F
x_{0,0} x_{0,1} ... x_{0,N-1}
...
x_{N-1,0} x_{N-1,1} ... x_{N-1,N-1}
```

- `N` is the size of the square input grid. It is always divisible by `F`.
- `F` is the size of the pooling window, and also the stride.
- The next `N` lines each hold `N` space-separated floats: the feature map `X`.

### Output Format

Print `M` lines, each holding `M` space-separated floats: the downsampled feature map `Y`.

Print every value with exactly **2 decimal places**.

**Judging:** accepted if the output matches the reference solution exactly.

---

### Constraints

- `1 <= F <= N <= 1000`
- `N` is divisible by `F`
- `-10^6 <= x <= 10^6` for every value in `X`
- Time limit: 1.0 second. Memory limit: 64 MB.

---

### Example 1

**Input**

```
4 2
1.0 2.0 0.5 0.1
3.0 4.0 1.5 1.1
0.0 -1.0 5.0 2.0
2.0 1.0 3.0 4.0
```

**Output**

```
4.00 1.50
2.00 5.00
```

**Explanation:** The `4 x 4` input is split into four `2 x 2` patches.

- Top-left patch: `max(1.0, 2.0, 3.0, 4.0) = 4.00`
- Top-right patch: `max(0.5, 0.1, 1.5, 1.1) = 1.50`
- Bottom-left patch: `max(0.0, -1.0, 2.0, 1.0) = 2.00`
- Bottom-right patch: `max(5.0, 2.0, 3.0, 4.0) = 5.00`

---

### Example 2

**Input**

```
4 4
-3.5 -2.0 -7.25 -1.5
-9.0 -4.0 -6.0 -8.0
-2.5 -3.0 -1.25 -5.0
-7.0 -6.5 -4.5 -2.75
```

**Output**

```
-1.25
```

**Explanation:** The window covers the whole grid, so the output is a single value: the largest of
the sixteen. Every value is negative, and the largest is `-1.25`, not `0`.

## Theory

### What max pooling does

A pooling layer slides a window over a feature map and replaces each window with one number. Max
pooling picks the largest value in the window. A large value in a feature map means a detector
fired strongly there, so keeping the maximum keeps the "something is here" signal and throws away
the exact position inside the window. That is the trade: the map gets `F` times smaller in each
direction, which is `F * F` times fewer values, and a small shift of a bright spot within a window
does not change the output.

### Output size

With window `F` and stride `F`, the windows tile the grid exactly, so an `N x N` map gives an
`M x M` map with `M = N / F`. Use integer division: `M = N // F`. The problem guarantees `F`
divides `N`, so nothing is left over at the edges.

### The starting value of the running maximum

Scanning a window keeps a running maximum, and it needs a starting value. Starting at `0.0` looks
harmless and is wrong: if every value in a window is negative, nothing beats `0.0`, and the output
is `0.0`, a value that was never in the window. Start at negative infinity, `float("-inf")`, or
at the first element of the window. Either way the running maximum can only ever be a real value
from the window.

### Indexing the window

Output cell `(i, j)` covers rows `i*F` up to `i*F + F - 1` and columns `j*F` up to `j*F + F - 1`.
Two nested loops over `a` and `b` in `range(F)` reach `X[i*F + a][j*F + b]`. The two edge cases are
the ones that expose off-by-one mistakes:

- `F = 1`: every window is one cell, so the output is a copy of the input.
- `F = N`: there is a single window, so the output is one number, the maximum of the whole grid.

### Cost

Every input cell is read exactly once, so the work is `N * N` regardless of `F`. At `N = 1000`
that is one million reads. Read the cells by index and avoid building a fresh list for every
window: copying a patch out before taking its maximum allocates a new list for each of the
`M * M` windows, which adds up on a grid this size.

## Explanation

`max_pool` reads the size `n` from the number of rows and computes `m = n // f`. It builds the
output one row at a time. For each output cell `(i, j)` it sets `best` to negative infinity, then
loops `a` over the window's rows and `b` over its columns, reading `matrix[i * f + a][j * f + b]`
and replacing `best` whenever it sees something larger. Starting from negative infinity means a
window of all negative values returns its real maximum instead of `0.0`.

No window is copied and nothing is sliced: each input cell is read once, by index, so the extra
memory is just the `m x m` output. With `f = 1` each window is a single cell and the output is an
equal copy of the input, and with `f = n` there is one window and the output is a single value.
