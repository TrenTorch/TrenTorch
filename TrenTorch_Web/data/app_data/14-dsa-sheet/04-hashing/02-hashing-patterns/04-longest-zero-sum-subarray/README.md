---
name: sheet-longest-zero-sum-subarray
title: 'Longest Zero-Sum Subarray'
tags: [dsa-sheet, hashing, hashing-patterns]
difficulty: Intermediate
theory: equal-prefix-sums-mean-a-zero-run
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

## Explanation

`first` starts with `{0: -1}` (the empty prefix before index 0). For each index update `prefix`; if it was seen before, the run from `first[prefix] + 1` to `i` sums to zero with length `i - first[prefix]`; otherwise store `first[prefix] = i`.

### Complexity

- Time: O(n). One pass; the first index of each prefix sum is stored and a repeated sum closes a zero-sum subarray.
- Space: O(n). The dictionary of first positions of prefix sums.
