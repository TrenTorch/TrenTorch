---
name: sheet-house-robber-ii
title: 'House Robber on a Circle'
tags: [dsa-sheet, dynamic-programming, sequences-and-counting]
difficulty: Intermediate
theory: house-robber-on-a-circle
---

## Statement

The houses now stand in a **circle**: the last house is a neighbour of the first. You still cannot rob two neighbouring houses. Return the **largest total** you can take.

For `[2, 3, 2]` the answer is `3` (houses 0 and 2 are neighbours).

### Examples

**Example 1**

Input:

```python
rob_circle([2, 3, 2])
```

Output:

```text
3
```

**Example 2**

Input:

```python
rob_circle([1, 2, 3, 1])
```

Output:

```text
4
```

### Constraints

- `0 <= len(nums) <= 300000`
- `0 <= nums[i] <= 10000`

## Explanation

`line` is the previous question's loop. The answer is the larger of the two lines that each drop one end.

### Complexity

- Time: O(n). Two passes of the house-robber scan: one without the first house, one without the last.
- Space: O(n). The two slices of the list.
