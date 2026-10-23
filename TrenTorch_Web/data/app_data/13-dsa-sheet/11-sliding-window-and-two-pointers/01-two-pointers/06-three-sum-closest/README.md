---
name: sheet-three-sum-closest
title: 'Three Sum Closest'
tags: [dsa-sheet, two-pointers, two-pointers]
difficulty: Intermediate
---

## Statement

Choose **three different positions** of `nums` and return the **sum that is closest to `target`**. If two sums are equally close, return the **smaller** one.

For `nums = [-1, 2, 1, -4]` and `target = 1` the answer is `2` (`-1 + 2 + 1`).

The starter code tries every triple. It is correct but too slow for long lists.

### Examples

**Example 1**

Input:

```python
three_sum_closest([-1, 2, 1, -4], 1)
```

Output:

```text
2
```

**Example 2**

Input:

```python
three_sum_closest([0, 0, 0], 1)
```

Output:

```text
0
```

### Constraints

- `3 <= len(nums) <= 1000`
- `-1000 <= nums[i] <= 1000`
- `-3000 <= target <= 3000`

## Theory

**Two pointers** means keeping two positions in the data (often one at each end, or one behind the other) and moving them according to a rule, so that each position moves at most `n` times in total. That turns a double loop (`O(n²)`) into a single pass (`O(n)`).

Sort `nums`. Fix the first number `nums[i]`; the other two come from the rest, which is sorted, so use **two pointers** `lo` (just after `i`) and `hi` (the end). The sum `s = nums[i] + nums[lo] + nums[hi]` tells which pointer to move: if `s < target` a bigger sum is needed, so `lo += 1`; if `s > target`, `hi -= 1`; if `s == target`, you cannot do better. Keep the best sum seen.

The loop over `i` is `O(n)` and each pointer pass is `O(n)`: `O(n²)` overall, instead of `O(n³)` for all triples.

## Explanation

Ties go to the smaller sum with the key `(abs(s - target), s)`. Each pointer pass moves `lo` or `hi` until they meet.
