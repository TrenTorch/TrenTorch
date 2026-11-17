---
name: sheet-find-the-duplicate-number
title: 'Find the Duplicate Number'
tags: [dsa-sheet, two-pointers, two-pointers]
difficulty: Advanced
theory: a-list-that-loops
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

## Explanation

`slow = nums[slow]` and `fast = nums[nums[fast]]` follow the "next" function. The second phase finds the cycle entrance.

### Complexity

- Time: O(n). Floyd's cycle detection on the 'index -> value' graph.
- Space: O(1). Two pointers; the list is not changed.
