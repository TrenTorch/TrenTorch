---
name: sheet-three-sum
title: 'Three Sum'
tags: [dsa-sheet, arrays, hard-arrays]
difficulty: Advanced
---

## Statement

Return all the **different triples of values** from `nums` that add up to `0`. Each triple is written in increasing order, there must be no repeated triple, and the list of triples is sorted (compare the first value, then the second, then the third). A value can be used as many times as it appears in `nums`, but only at different positions.

The starter code tries every set of three positions. It is correct but too slow for long lists. Make it fast.

### Examples

**Example 1**

Input:

```python
three_sum([-1, 0, 1, 2, -1, -4])
```

Output:

```text
[[-1, -1, 2], [-1, 0, 1]]
```

The triples are `[-1, -1, 2]` and `[-1, 0, 1]`.

**Example 2**

Input:

```python
three_sum([0, 0, 0, 0])
```

Output:

```text
[[0, 0, 0]]
```

Only one different triple: `[0, 0, 0]`.

### Constraints

- `0 <= len(nums) <= 1500`
- `-10**5 <= nums[i] <= 10**5`

## Theory

Three nested loops are `O(n³)`. **Sort first.** Once the list is sorted, fix the smallest value `a[i]` and look for two values to its right that add up to `-a[i]`. Finding a pair with a given sum in a sorted list takes `O(n)` with **two pointers**: one at each end. If the sum is too small, move the left pointer right; if it is too big, move the right pointer left.

Do that for each `i` and the total is `O(n²)`.

Duplicates are the tricky part. Skip a value for `i` if it equals the previous one (it would produce the same triples). After you find a triple, move both pointers and skip over equal values on each side. Sorting is what makes all of those skips simple: equal values are adjacent.

## Explanation

Sort, then for each `i` (skipping repeated `a[i]`) run two pointers `lo = i + 1` and `hi = n - 1`. Too small: `lo += 1`. Too big: `hi -= 1`. On a match, record the triple, step both pointers, then skip equal values at `lo` and `hi`. The triples come out in sorted order automatically because `i`, then `lo`, only move forward.
