---
name: sheet-union-sorted
title: 'Union of Two Sorted Lists'
tags: [dsa-sheet, arrays, array-basics]
difficulty: Beginner
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

## Theory

With a `set` you could write `sorted(set(a) | set(b))`, which costs `O(n log n)`. Because both lists are already sorted, you can **merge** them in `O(n)` like the merge step of merge sort, and skip repeats as you go.

Walk both lists with two pointers. Take the smaller current value (from `a` on a tie), and add it to the answer only if it differs from the last value added. Because the output is built in increasing order, a repeat is always equal to the last value added.

## Explanation

Each round picks the next value: from `a` if `b` is used up or `a[i] <= b[j]`, otherwise from `b`. Then it appends the value unless it equals the last appended value. Loop until both lists are used up.
