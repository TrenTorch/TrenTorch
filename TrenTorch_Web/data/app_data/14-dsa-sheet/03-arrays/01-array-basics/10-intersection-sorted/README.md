---
name: sheet-intersection-sorted
title: 'Common Values of Two Sorted Lists'
tags: [dsa-sheet, arrays, array-basics]
difficulty: Beginner
theory: finding-what-two-lists-share
---

## Statement

`a` and `b` are sorted in non-decreasing order. Return a sorted list of the values they **share**, where a value that appears `x` times in `a` and `y` times in `b` appears `min(x, y)` times in the result.

### Examples

**Example 1**

Input:

```python
intersection_sorted([1, 2, 2, 3], [2, 2, 2, 4])
```

Output:

```text
[2, 2]
```

`2` appears twice in `a` and three times in `b`, so it appears twice.

**Example 2**

Input:

```python
intersection_sorted([1, 2], [3, 4])
```

Output:

```text
[]
```

### Constraints

- `0 <= len(a), len(b) <= 2 * 10**5`
- Both lists are sorted in non-decreasing order.

## Explanation

Equal values are appended and both positions advance, which is what gives `min(x, y)` copies of a repeated value. A smaller value on either side is skipped.

### Complexity

- Time: O(n + m). Two pointers move forward through the sorted lists.
- Space: O(min(n, m)). The result list can hold at most the shorter list.
