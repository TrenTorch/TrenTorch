---
name: sheet-sort-k-sorted-array
title: 'Sort a Nearly Sorted Array'
tags: [dsa-sheet, heaps, heap-basics]
difficulty: Intermediate
theory: a-sliding-buffer-for-nearly-sorted-data
---

## Statement

Every value of `nums` is at most `k` positions away from the position it would have in the **sorted** list. Return the sorted list. Aim for `O(n log k)` time.

For `nums = [6, 5, 3, 2, 8, 10, 9]` and `k = 3` the answer is `[2, 3, 5, 6, 8, 9, 10]`.

### Examples

**Example 1**

Input:

```python
sort_k_sorted([6, 5, 3, 2, 8, 10, 9], 3)
```

Output:

```text
[2, 3, 5, 6, 8, 9, 10]
```

**Example 2**

Input:

```python
sort_k_sorted([3, 2, 1], 2)
```

Output:

```text
[1, 2, 3]
```

### Constraints

- `0 <= len(nums) <= 100000`
- `0 <= k <= len(nums)`
- `-10**9 <= nums[i] <= 10**9`

## Explanation

The first `k + 1` values go into the heap; afterwards every step pushes one value and pops one. The pops come out in sorted order.

### Complexity

- Time: O(n log k). A heap of `k + 1` values always holds the next smallest, `O(log k)` per value.
- Space: O(k). The heap (the result is output).
