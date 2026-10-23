---
name: sheet-next-greater-circular
title: 'Next Greater Element in a Circle'
tags: [dsa-sheet, stack-and-queue, monotonic-stack]
difficulty: Intermediate
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

## Theory

A **stack** is last in, first out: you only add (`push`) and remove (`pop`) at the top. In Python a list does this with `append()` and `pop()`, both `O(1)`.

A circle can be handled by **walking the list twice**. Run the usual monotonic stack over indices `0 .. 2n - 1`, using `nums[i % n]` as the value. Only push an index in the first lap (`i < n`): the second lap is only there to answer the indices still waiting.

Everything else is the same as in the plain next greater element question. `O(n)`.

## Explanation

In the second lap values only answer waiting indices; they are not pushed again, so every index is answered at most once.
