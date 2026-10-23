---
name: sheet-longest-zero-sum-subarray
title: 'Longest Zero-Sum Subarray'
tags: [dsa-sheet, hashing, hashing-patterns]
difficulty: Intermediate
---

## Statement

Return the length of the **longest contiguous run** of `nums` whose values add up to `0`, or `0` if there is none. Values can be negative.

The starter code tries every start and end. It is correct but too slow. Make it fast.

### Examples

**Example 1**

Input:

```python
longest_zero_sum_subarray([15, -2, 2, -8, 1, 7, 10, 23])
```

Output:

```text
5
```

The run `[-2, 2, -8, 1, 7]` adds to 0 and has length 5.

**Example 2**

Input:

```python
longest_zero_sum_subarray([1, 2, 3])
```

Output:

```text
0
```

No run adds to 0.

### Constraints

- `0 <= len(nums) <= 2 * 10**5`
- `-10**4 <= nums[i] <= 10**4`

## Theory

A run adds up to `0` exactly when the prefix sum **before** it equals the prefix sum **after** it. So you are looking for the two positions with the **same prefix sum** that are the farthest apart.

Keep a dictionary of the **first** index where each prefix sum appeared. When a prefix sum appears again at index `i`, the run between the first occurrence and `i` adds up to zero, and its length is `i - first[prefix]`. Never overwrite the first index: you want the longest run.

This is the `k = 0` case of the prefix-sum trick, and the first place most people see why "store the first index" matters.

## Explanation

`first` starts with `{0: -1}` (the empty prefix before index 0). For each index update `prefix`; if it was seen before, the run from `first[prefix] + 1` to `i` sums to zero with length `i - first[prefix]`; otherwise store `first[prefix] = i`.
