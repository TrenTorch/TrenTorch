---
name: sheet-next-greater-element
title: 'Next Greater Element'
tags: [dsa-sheet, stack-and-queue, stack-basics]
difficulty: Intermediate
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

## Theory

A **stack** is last in, first out: you only add (`push`) and remove (`pop`) at the top. In Python a list does this with `append()` and `pop()`, both `O(1)`.

Scanning right from every element repeats work: `O(n²)`. A **monotonic stack** answers all positions in one pass. Walk the list from left to right and keep the **indices still waiting for their answer**. These indices always have values that do not increase from bottom to top (that is why the stack is "monotonic").

For each new value `x`, it is the next greater element of every waiting index whose value is smaller: **pop** them one by one and set their answer to `x`. Then push the current index to wait. Indices left in the end have no greater value: `-1`.

Each index is pushed once and popped once, so the whole thing is `O(n)`. This pattern solves a whole family of "nearest bigger/smaller" questions.

## Explanation

The stack holds indices of values still without an answer, in non-increasing order of value. A new value that is bigger than the top answers it, and keeps answering the new top while it is bigger.
