---
name: sheet-jump-game
title: 'Jump Game'
tags: [dsa-sheet, greedy, greedy-basics]
difficulty: Intermediate
theory: jump-game
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

## Explanation

Every index up to `far` is reachable, because you can reach `far` by some jump and shorter jumps land on everything in between. An index past `far` can never be reached.

### Complexity

- Time: O(n). One pass keeping the furthest reachable index.
- Space: O(1). One integer.
