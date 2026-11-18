---
name: sheet-sum-of-subarray-minimums
title: 'Sum of Subarray Minimums'
tags: [dsa-sheet, stack-and-queue, monotonic-stack]
difficulty: Advanced
theory: counting-by-contribution
---

## Statement

Return the **sum of `min(subarray)` over every contiguous subarray** of `arr`, modulo `10**9 + 7`.

For `[3, 1, 2, 4]` the subarray minimums are `3, 1, 2, 4, 1, 1, 2, 1, 1, 1`, whose sum is `17`.

The starter code visits every subarray. It is correct but too slow for long arrays.

### Examples

**Example 1**

Input:

```python
sum_subarray_mins([3, 1, 2, 4])
```

Output:

```text
17
```

**Example 2**

Input:

```python
sum_subarray_mins([11, 81, 94, 43, 3])
```

Output:

```text
444
```

### Constraints

- `0 <= len(arr) <= 200000`
- `1 <= arr[i] <= 30000`

## Explanation

One stack pass computes `left` while scanning and `right` when elements are popped; here both are computed with two passes for clarity.

### Complexity

- Time: O(n). Two monotonic-stack passes find, for every element, how far it stays the minimum on each side.
- Space: O(n). The two boundary arrays and the stack.
