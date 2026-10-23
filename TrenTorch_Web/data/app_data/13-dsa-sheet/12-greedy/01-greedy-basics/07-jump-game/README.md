---
name: sheet-jump-game
title: 'Jump Game'
tags: [dsa-sheet, greedy, greedy-basics]
difficulty: Intermediate
---

## Statement

You start at index 0 of `nums`. The value `nums[i]` is the **maximum jump length** from index `i` (you may jump any shorter distance too). Return `True` if you can reach the **last index**.

For `[2, 3, 1, 1, 4]` the answer is `True`; for `[3, 2, 1, 0, 4]` it is `False`.

The starter code works backwards and scans many positions for every index. It is correct but too slow for long lists.

### Examples

**Example 1**

Input:

```python
can_jump([2, 3, 1, 1, 4])
```

Output:

```text
True
```

**Example 2**

Input:

```python
can_jump([3, 2, 1, 0, 4])
```

Output:

```text
False
```

### Constraints

- `0 <= len(nums) <= 200000`
- `0 <= nums[i] <= 100000`

## Theory

A **greedy** algorithm builds the answer step by step and, at each step, takes the choice that looks best **right now**, without ever going back. It is fast and simple, but it is only correct when the problem has a structure that makes local choices safe. The hard part is the **proof**: show that the greedy choice can always be part of some best answer.

You do not need to know _which_ jumps to make, only whether the end is reachable. Keep `far`, the **farthest index you can reach** so far. Scan the indices from left to right: if you reach an index `i` that is **beyond** `far`, you are stuck, so return `False`. Otherwise update `far = max(far, i + nums[i])`.

If `far` reaches the last index, return `True`. `O(n)` time and `O(1)` memory, instead of trying all jump sequences.

## Explanation

Every index up to `far` is reachable, because you can reach `far` by some jump and shorter jumps land on everything in between. An index past `far` can never be reached.
