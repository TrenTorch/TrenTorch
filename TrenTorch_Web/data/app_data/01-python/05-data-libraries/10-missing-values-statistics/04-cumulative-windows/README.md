---
name: numpy-cumulative-windows
title: 'Cumulative Operations & Moving Windows'
tags: [numpy-core]
difficulty: Intermediate
---

## Statement

Implement running and windowed statistics for a 1D series without a Python loop over positions. `running_total` is the cumulative sum, `cumulative_max` the running maximum, `consecutive_differences` the change between neighbours, `percent_change` the relative change from each value to the next (with `NaN` where the previous value is `0`), and `moving_average` the mean of every window of `w` consecutive values, computed with the cumulative-sum trick so that the cost does not grow with `w`.

## Theory

### Cumulative operations

`np.cumsum(a)` returns the running total, `np.cumprod` the running product, and `np.maximum.accumulate(a)` the running maximum:

```python
a = np.array([3, 1, 4, 1, 5])
np.cumsum(a)                # [ 3,  4,  8,  9, 14]
np.maximum.accumulate(a)    # [ 3,  3,  4,  4,  5]
```

### Differences

`np.diff(a)` gives `a[1:] - a[:-1]`, one element shorter than `a`. The running total undoes it: `a[0] + np.cumsum(np.diff(a))` rebuilds `a[1:]`. Dividing the differences by the previous values gives the relative change (for example daily returns):

$$
\text{change}_t = \frac{x_t - x_{t-1}}{x_{t-1}}
$$

which is undefined when $x_{t-1} = 0$, so those positions are `NaN`.

### Moving averages without a loop

A window of $w$ values sliding along $n$ values has $n-w+1$ positions. Summing each window by brute force costs $O(nw)$. With the **cumulative sum** $C_i = x_0 + \dots + x_{i-1}$ (and $C_0 = 0$), every window sum is a difference of two entries:

$$
\sum_{j=i}^{i+w-1} x_j = C_{i+w} - C_{i}
$$

so all window means are `(C[w:] - C[:-w]) / w`, computed in $O(n)$ for any $w$.

```python
c = np.concatenate(([0], np.cumsum(a)))
(c[w:] - c[:-w]) / w
```

### Floating-point caution

The cumulative trick subtracts large running totals, which loses precision when values are huge or the series is very long. For well-scaled data it is accurate; for extreme ranges prefer `np.lib.stride_tricks.sliding_window_view(a, w).mean(axis=1)`.

### How NumPy implements this

`cumsum` and `accumulate` are single sequential passes in C. `diff` is a vectorised subtraction of two shifted views, so it allocates one new array and never copies the input twice.

## Explanation

`running_total` is `np.cumsum`. `cumulative_max` uses `np.maximum.accumulate`. `consecutive_differences` is `np.diff`. `percent_change` divides those differences by the previous values, writing `NaN` where the previous value is zero. `moving_average` prepends a zero to the cumulative sum and subtracts entries `w` apart, so each window sum is a difference of two numbers and the result has `n - w + 1` entries.
