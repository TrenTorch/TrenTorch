---
name: sheet-remove-duplicates-at-most-twice
title: 'Keep at Most Two of Each Value'
tags: [dsa-sheet, two-pointers, two-pointers]
difficulty: Intermediate
theory: a-reader-and-a-writer
---

## Statement

`nums` is sorted in increasing order. Return the list where each value appears **at most twice** (extra copies removed), keeping the order. For `[1, 1, 1, 2, 2, 3]` the answer is `[1, 1, 2, 2, 3]`.

Try to solve it with one pass and two pointers: a **write** pointer for the answer and a **read** pointer for the input.

### Examples

**Example 1**

Input:

```python
keep_at_most_twice([1, 1, 1, 2, 2, 3])
```

Output:

```text
[1, 1, 2, 2, 3]
```

**Example 2**

Input:

```python
keep_at_most_twice([0, 0, 1, 1, 1, 1, 2, 3, 3])
```

Output:

```text
[0, 0, 1, 1, 2, 3, 3]
```

### Constraints

- `0 <= len(nums) <= 200000`
- `nums` is sorted in increasing order.

## Explanation

`a[write - 2]` is the second-to-last kept value. If the new value differs from it, there are fewer than two copies of the new value kept (the list is sorted), so it can be kept.

### Complexity

- Time: O(n). One pass; a value is kept unless the value two places behind the write position equals it.
- Space: O(n). A copy of the list is made because the input must not change.
