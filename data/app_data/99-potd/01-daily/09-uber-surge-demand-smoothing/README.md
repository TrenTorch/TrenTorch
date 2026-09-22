---
name: vision-pool-uber-surge-demand-smoothing
title: 'UBER SURGE: DEMAND SMOOTHING'
tags: [computer-vision, pooling, array-manipulation, spatial-data]
difficulty: Beginner
---

## Statement

**Difficulty:** Easy
**Tags:** Computer Vision, Average Pooling, Spatial Data, Array Manipulation

---

### Story

Uber's dynamic pricing (surge pricing) divides a city into a high-resolution spatial grid to track
ride requests in real time. During a major event, a single city block can see a massive, localized
spike in demand. If the surge model reacts to that one block alone, riders get a fragmented
experience where crossing the street changes the price drastically.

To avoid this fragmentation, Uber's marketplace models use **Average Pooling** to smooth and
downsample the spatial demand features before they reach forecasting models like DeepETA. This is
the same operation as `02-average-pooling` in the Vision track, written from scratch. By averaging
demand over local patches, you smooth out extreme local spikes and shrink the grid for faster
downstream inference.

---

### The Math: Average Pooling

Given an `N x N` input matrix `X` (the high-resolution demand grid) and a pooling window of size
`F`, with a stride equal to `F` (the windows do not overlap), the output `Y` is an `M x M` matrix
where `M = N / F`.

For every output position `(i, j)` with `0 <= i < M` and `0 <= j < M`, the value is the arithmetic
mean of the matching `F x F` patch of the input:

```
Y[i][j] = mean( X[i*F + a][j*F + b] )   over all 0 <= a < F and 0 <= b < F
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
- The next `N` lines each hold `N` space-separated floats: the demand grid `X`.

### Output Format

Print `M` lines, each holding `M` space-separated floats: the smoothed, downsampled grid `Y`.

Print every value with exactly **4 decimal places**.

**Judging:** accepted if every output value is within `1e-4` absolute error of the reference
solution.

---

### Constraints

- `1 <= F <= N <= 1000`
- `N` is divisible by `F`
- values of `X` can be negative (normalized, z-scored demand)
- Time limit: 1.0 second. Memory limit: 64 MB.

---

### Example 1

**Input**

```
4 2
10.0 20.0 5.0 1.0
30.0 40.0 1.0 1.0
0.0 0.0 50.0 20.0
0.0 0.0 10.0 40.0
```

**Output**

```
25.0000 2.0000
0.0000 30.0000
```

**Explanation:** The `4 x 4` input is split into four `2 x 2` patches.

- Top-left patch: `(10.0 + 20.0 + 30.0 + 40.0) / 4 = 25.0000`: a strong, localized demand spike is
  smoothed out over the neighborhood.
- Top-right patch: `(5.0 + 1.0 + 1.0 + 1.0) / 4 = 2.0000`
- Bottom-left patch: `(0.0 + 0.0 + 0.0 + 0.0) / 4 = 0.0000`
- Bottom-right patch: `(50.0 + 20.0 + 10.0 + 40.0) / 4 = 30.0000`

## Theory

### Average pooling, not max pooling

`01-max-pooling` keeps a patch's single largest value and throws away the rest, the right choice
when one strong reading anywhere in the patch matters, like a hot engine in a thermal image. Demand
is different: one block ordering four times as many rides as its neighbors is real signal, but
letting that one block set the price for the whole patch is exactly the fragmentation the story
describes. Averaging blends every cell in the patch into one number, so a single spike is smoothed
rather than dictating the output.

### Output size

With window `F` and stride `F`, the windows tile the grid exactly, so an `N x N` grid gives an
`M x M` grid with `M = N / F`. Use integer division: `M = N // F`. `F` is guaranteed to divide `N`,
so there is no partial window at an edge.

### Summing before dividing

The mean of an `F x F` patch is its sum divided by `F * F`, not by `F`, since a patch has `F * F`
cells, not `F`. Accumulate the sum first, then divide once per output cell.

### Negative values do not need special handling

Unlike max pooling, average pooling has no "wrong starting value" trap: a running sum correctly
starts at `0.0` whether the patch is all positive, all negative, or a mix, because summing is
associative regardless of sign. The risk with negative values is purely presentation: printing
`-0.0000` for a patch that sums to exactly zero is still correct, since `-0.0 == 0.0`.

### Floating-point accumulation on very large patches

For a small grid, the order of summation cannot change the answer within the judge's `1e-4`
tolerance. On a sparse grid where a `1000 x 1000` input is almost entirely `0.0` with a few large
values, accumulating the patch sum as a single running total (rather than, say, summing in a
different order per call) keeps the result stable and matches a NumPy reference computed the same
way.

### Two edge cases

- `F = 1`: every window is one cell, so the output equals the input exactly (dividing one value by
  `1` changes nothing).
- `F = N`: there is a single window, so the output is one value, the mean of the entire grid.

### Cost

Every input cell is read exactly once, so the work is `N * N` regardless of `F`. At `N = 1000` that
is one million reads. As with max pooling, read cells by index rather than slicing a fresh patch
out of the grid for every window: slicing allocates a new list for each of the `M * M` windows,
which adds up at this size. A streaming implementation that only keeps `F` rows of the input in
memory at a time can compute the same output while reading the grid a row at a time, which is how
this fits comfortably inside the 64 MB limit even at `N = 1000`.

## Explanation

`avg_pool` reads the grid size `n` from the number of rows and computes `m = n // f`. It builds the
output one row at a time. For each output cell `(i, j)` it accumulates `total`, starting at `0.0`,
by looping `a` over the window's rows and `b` over its columns and adding
`matrix[i * f + a][j * f + b]`. Once both loops finish it appends `total / (f * f)` to the output
row, dividing by the patch's cell count rather than by `f`.

No window is copied and nothing is sliced: each input cell is read once, by index, so the extra
memory is just the `m x m` output. Because addition does not care about sign, the same accumulation
handles positive, negative, and mixed patches without a special case. With `f = 1` each window is a
single cell divided by `1`, an exact copy of the input, and with `f = n` there is one window and the
output is a single value, the mean of the whole grid.
