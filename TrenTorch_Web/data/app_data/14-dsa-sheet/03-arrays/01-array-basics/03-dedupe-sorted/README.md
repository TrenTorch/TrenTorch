---
name: sheet-dedupe-sorted
title: 'Remove Duplicates From Sorted'
tags: [dsa-sheet, arrays, array-basics]
difficulty: Beginner
theory: using-the-sorted-order
---

## Statement

`nums` is sorted in non-decreasing order. Return a new list with each value kept **once**, still in order. Do not use `set`: use the fact that the list is sorted.

### Examples

**Example 1**

Input:

```python
dedupe_sorted([1, 1, 2, 2, 2, 3])
```

Output:

```text
[1, 2, 3]
```

**Example 2**

Input:

```python
dedupe_sorted([4, 4, 4])
```

Output:

```text
[4]
```

### Constraints

- `0 <= len(nums) <= 3 * 10**5`
- `nums` is sorted in non-decreasing order.

## Explanation

`out[-1]` is the last kept value. A new value is appended only when `out` is empty or the value differs from `out[-1]`. Sortedness guarantees that a repeated value is always adjacent to its twin.

### Complexity

- Time: O(n). One pass, comparing each value with the last one kept.
- Space: O(n). The result list holds up to `n` values.
