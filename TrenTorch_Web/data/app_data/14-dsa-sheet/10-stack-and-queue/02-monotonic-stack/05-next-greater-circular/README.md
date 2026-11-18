---
name: sheet-next-greater-circular
title: 'Next Greater Element in a Circle'
tags: [dsa-sheet, stack-and-queue, monotonic-stack]
difficulty: Intermediate
theory: going-around-a-circle
---

## Statement

The list is **circular**: after the last element comes the first one again. For each value, find the **next strictly greater value**, looking to the right and wrapping around the end if needed; return `-1` if there is none.

For `[1, 2, 1]` the answer is `[2, -1, 2]`.

### Examples

**Example 1**

Input:

```python
next_greater_circular([1, 2, 1])
```

Output:

```text
[2, -1, 2]
```

**Example 2**

Input:

```python
next_greater_circular([1, 2, 3, 4, 3])
```

Output:

```text
[2, 3, 4, -1, 4]
```

### Constraints

- `0 <= len(nums) <= 200000`
- `-10**9 <= nums[i] <= 10**9`

## Explanation

In the second lap values only answer waiting indices; they are not pushed again, so every index is answered at most once.

### Complexity

- Time: O(n). Two laps over the array, each index pushed once and popped at most once.
- Space: O(n). The stack and the result.
