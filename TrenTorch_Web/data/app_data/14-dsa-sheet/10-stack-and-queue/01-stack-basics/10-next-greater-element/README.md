---
name: sheet-next-greater-element
title: 'Next Greater Element'
tags: [dsa-sheet, stack-and-queue, stack-basics]
difficulty: Intermediate
theory: a-waiting-room
---

## Statement

For every value in `nums`, find the **first value to its right that is strictly greater**, and return a list of those values (`-1` where there is none).

For `[2, 1, 2, 4, 3]` the answer is `[4, 2, 4, -1, -1]`.

The starter code scans to the right from every position. It is correct but too slow for long lists.

### Examples

**Example 1**

Input:

```python
next_greater([2, 1, 2, 4, 3])
```

Output:

```text
[4, 2, 4, -1, -1]
```

**Example 2**

Input:

```python
next_greater([3, 2, 1])
```

Output:

```text
[-1, -1, -1]
```

### Constraints

- `0 <= len(nums) <= 200000`
- `-10**9 <= nums[i] <= 10**9`

## Explanation

The stack holds indices of values still without an answer, in non-increasing order of value. A new value that is bigger than the top answers it, and keeps answering the new top while it is bigger.

### Complexity

- Time: O(n). Each index is pushed once and popped at most once.
- Space: O(n). The stack and the result.
