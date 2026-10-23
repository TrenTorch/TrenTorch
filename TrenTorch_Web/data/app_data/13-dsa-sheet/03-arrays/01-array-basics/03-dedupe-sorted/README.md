---
name: sheet-dedupe-sorted
title: 'Remove Duplicates From Sorted'
tags: [dsa-sheet, arrays, array-basics]
difficulty: Beginner
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

## Theory

In a sorted list, equal values sit **next to each other**. So you never need to remember every value you have seen (which is what a `set` does). It is enough to compare each value with the **last one you kept**: if it differs, keep it; if it is the same, skip it.

This is the **two-pointer** idea: one pointer reads every value, and another marks where the next kept value goes. In Python the "write pointer" is simply the end of the result list. It runs in `O(n)` time and needs no hashing.

## Explanation

`out[-1]` is the last kept value. A new value is appended only when `out` is empty or the value differs from `out[-1]`. Sortedness guarantees that a repeated value is always adjacent to its twin.
