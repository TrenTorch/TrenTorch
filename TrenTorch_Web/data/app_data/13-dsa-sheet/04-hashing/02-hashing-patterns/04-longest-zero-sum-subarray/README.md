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

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                       | Variables                                                                        |
| ------------------------------------- | -------------------------------------------------------------------------------- |
| `first = {0: -1}`                     | `first = {0: -1}`                                                                |
| `first[prefix] = i`                   | `first = {0: -1, 15: 0}, prefix = 15, best = 0, i = 0, x = 15`                   |
| `first[prefix] = i`                   | `first = {0: -1, 15: 0, 13: 1}, prefix = 13, i = 1, x = -2`                      |
| `for i, x in enumerate(nums):`        | `prefix = 15, best = 2, i = 3, x = -8`                                           |
| `prefix += x`                         | `first = {0: -1, 15: 0, 13: 1, 7: 3}, prefix = 8, i = 4, x = 1`                  |
| `best = max(best, i - first[prefix])` | `first = {0: -1, 15: 0, 13: 1, 7: 3, 8: 4}, prefix = 15, best = 5, i = 5, x = 7` |
| `first[prefix] = i`                   | `first = {0: -1, 15: 0, 13: 1, 7: 3, 8: 4, 25: 6}, prefix = 25, i = 6, x = 10`   |
| `return`                              | `returned = 5`                                                                   |

### Complexity

- Time: O(n) where n is the length of nums.
- Extra space: O(n) where n is the length of nums.
- The brute force takes O(n^2) where n is the length of nums.
