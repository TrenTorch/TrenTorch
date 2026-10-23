---
name: sheet-max-product-subarray
title: 'Maximum Product Subarray'
tags: [dsa-sheet, arrays, hard-arrays]
difficulty: Advanced
---

## Statement

Return the largest **product** of a contiguous, non-empty run of `nums`. Values can be negative or zero.

The tests keep the product small for long lists (the values are `-1`, `0` and `1` there), and use values from `-2` to `2` for short lists.

### Examples

**Example 1**

Input:

```python
max_product_subarray([2, 3, -2, 4])
```

Output:

```text
6
```

The run `[2, 3]` has product 6.

**Example 2**

Input:

```python
max_product_subarray([-2, 0, -1])
```

Output:

```text
0
```

The best is `0`; neither `-2` nor `-1` alone is better.

### Constraints

- `1 <= len(nums) <= 2 * 10**5`
- `-2 <= nums[i] <= 2`

## Theory

Kadane's algorithm for the best **sum** keeps one running value. For products it is not enough, because a very **negative** product can become the best one when multiplied by another negative value.

So keep **two** running values for the run ending at the current position: the largest product `hi` and the smallest product `lo`. For a new value `x` the new run is one of: just `x`, `hi * x`, or `lo * x`. Take the max for the new `hi` and the min for the new `lo`. A negative `x` swaps their roles, which is handled automatically by taking max/min over all three candidates. A zero resets both to `0` and the run effectively starts again.

The answer is the best `hi` seen. One pass: `O(n)`.

## Explanation

`hi` and `lo` are the largest and smallest product of a run ending at the current value. The three candidates `x`, `hi * x`, `lo * x` cover starting a new run, extending the best run, and extending the worst run (useful when `x < 0`). `best` is the maximum `hi` seen.
