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

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line | Variables                          |
| --------------- | ---------------------------------- |
| `out = []`      | `out = []`                         |
| `i += 1`        | `i = 1, j = 0, x = 1`              |
| `i += 1`        | `out = [1], i = 2, x = 2`          |
| `j += 1`        | `out = [1, 2], i = 3, j = 1`       |
| `j += 1`        | `j = 2, x = 3`                     |
| `i += 1`        | `out = [1, 2, 3], i = 4, x = 4`    |
| `x = b[j]`      | `out = [1, 2, 3, 4], j = 3, x = 5` |
| `return`        | `returned = [1, 2, 3, 4, 5]`       |

### Complexity

- Time: O(n + m) n = len(a), m = len(b).
- Extra space: O(1) only constant extra variables.
- The brute force takes O((n + m) log (n + m)) n = len(a), m = len(b).
