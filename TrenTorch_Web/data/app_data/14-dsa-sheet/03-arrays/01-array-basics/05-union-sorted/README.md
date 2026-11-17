---
name: sheet-union-sorted
title: 'Union of Two Sorted Lists'
tags: [dsa-sheet, arrays, array-basics]
difficulty: Beginner
theory: merging-two-sorted-lists
---

## Statement

`a` and `b` are each sorted in non-decreasing order and may contain repeated values. Return a sorted list containing every value that appears in `a` **or** `b`, each exactly once.

### Examples

**Example 1**

Input:

```python
union_sorted([1, 2, 2, 4], [2, 3, 4, 5])
```

Output:

```text
[1, 2, 3, 4, 5]
```

**Example 2**

Input:

```python
union_sorted([], [1, 1])
```

Output:

```text
[1]
```

### Constraints

- `0 <= len(a), len(b) <= 2 * 10**5`
- Both lists are sorted in non-decreasing order.

## Explanation

Each round picks the next value: from `a` if `b` is used up or `a[i] <= b[j]`, otherwise from `b`. Then it appends the value unless it equals the last appended value. Loop until both lists are used up.

### Complexity

- Time: O(n + m). A merge of the two lists, each pointer only moves forward.
- Space: O(n + m). The result list; nothing else is allocated.
