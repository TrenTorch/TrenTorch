---
name: sheet-longest-increasing-subsequence
title: 'Longest Increasing Subsequence'
tags: [dsa-sheet, dynamic-programming, sequences-and-counting]
difficulty: Advanced
theory: the-faster-tails-idea
---

## Statement

Return the length of the **longest strictly increasing subsequence** of `nums` (a subsequence keeps the order but may skip values).

For `[10, 9, 2, 5, 3, 7, 101, 18]` the answer is `4` (`2, 3, 7, 18`).

The starter code compares every value with all earlier ones. It is correct but too slow for long lists.

### Examples

**Example 1**

Input:

```python
length_of_lis([10, 9, 2, 5, 3, 7, 101, 18])
```

Output:

```text
4
```

**Example 2**

Input:

```python
length_of_lis([7, 7, 7, 7])
```

Output:

```text
1
```

### Constraints

- `0 <= len(nums) <= 200000`
- `-10**9 <= nums[i] <= 10**9`

## Explanation

`bisect_left` finds the position where `x` belongs. Using `bisect_left` (not `bisect_right`) makes equal values replace each other, which enforces strictly increasing.

### Complexity

- Time: O(n log n). One binary search per value on the table of smallest tails.
- Space: O(n). The tails list.
