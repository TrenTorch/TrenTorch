---
name: sheet-find-the-duplicate-number
title: 'Find the Duplicate Number'
tags: [dsa-sheet, two-pointers, two-pointers]
difficulty: Advanced
---

## Statement

`nums` has `n + 1` values, each between `1` and `n`, so **exactly one value is repeated** (it may appear more than twice). Return that value **without changing `nums`** and with `O(1)` extra memory.

### Examples

**Example 1**

Input:

```python
find_duplicate([1, 3, 4, 2, 2])
```

Output:

```text
2
```

**Example 2**

Input:

```python
find_duplicate([3, 1, 3, 4, 2])
```

Output:

```text
3
```

### Constraints

- `2 <= len(nums) <= 200001`
- `1 <= nums[i] <= n` where `n = len(nums) - 1`
- Exactly one value appears more than once; all others appear once.

## Theory

Treat the list as a **linked list**: from position `i`, the next position is `nums[i]`. Because every value is in `1..n` and there are `n + 1` positions, every walk stays inside the array, and since two positions hold the same value, two different places lead to the **same next position**: the walk eventually enters a **cycle**, and the **entrance of the cycle is the duplicate** (it is the position reached from two different places).

That is exactly the linked list cycle question. Use Floyd's tortoise and hare: find the meeting point with slow (1 step) and fast (2 steps), then restart one pointer from position 0 and move both one step at a time until they meet again: the meeting value is the duplicate.

`O(n)` time and `O(1)` memory, without modifying the input.

## Explanation

`slow = nums[slow]` and `fast = nums[nums[fast]]` follow the "next" function. The second phase finds the cycle entrance.
