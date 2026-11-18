---
name: sheet-move-zeros
title: 'Move Zeros to the End'
tags: [dsa-sheet, arrays, array-basics]
difficulty: Beginner
theory: a-read-finger-and-a-write-finger
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

## Explanation

`[x for x in nums if x != 0]` keeps the non-zero values in order. `nums.count(0)` counts the zeros, and `[0] * count` builds the tail. Concatenate them.

### Complexity

- Time: O(n). One filter pass and one `count` pass.
- Space: O(n). The result list.
