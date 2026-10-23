---
name: sheet-move-zeros
title: 'Move Zeros to the End'
tags: [dsa-sheet, arrays, array-basics]
difficulty: Beginner
---

## Statement

Return a new list where every `0` has been moved to the **end**, and all other values keep their original relative order. Do not change `nums`.

### Examples

**Example 1**

Input:

```python
move_zeros([0, 1, 0, 3, 12])
```

Output:

```text
[1, 3, 12, 0, 0]
```

**Example 2**

Input:

```python
move_zeros([0, 0])
```

Output:

```text
[0, 0]
```

### Constraints

- `0 <= len(nums) <= 3 * 10**5`
- `-10**9 <= nums[i] <= 10**9`

## Theory

This is a **stable partition**: split the values into two groups (non-zero, then zero) without disturbing the order inside a group.

The simple way is two passes: collect the non-zero values, then add as many zeros as were removed. That is `O(n)` time. The classic in-place version uses two pointers: a read pointer scans every value, and a write pointer marks where the next non-zero value belongs; each non-zero value is swapped forward to the write position.

Python list comprehensions make the two-pass version short and fast. Know the in-place version too: interviews ask for it when memory is tight.

## Explanation

`[x for x in nums if x != 0]` keeps the non-zero values in order. `nums.count(0)` counts the zeros, and `[0] * count` builds the tail. Concatenate them.
