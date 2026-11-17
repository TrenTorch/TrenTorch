---
name: sheet-trapping-rain-water
title: 'Trapping Rain Water'
tags: [dsa-sheet, two-pointers, two-pointers]
difficulty: Advanced
theory: trapping-rain-water-with-two-pointers
---

## Statement

`heights[i]` is the height of a bar of width 1. After it rains, water collects between the bars. Return the **total amount of water trapped**.

For `[0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]` the answer is `6`.

The starter code searches both sides of every bar. It is correct but too slow for many bars.

### Examples

**Example 1**

Input:

```python
trap_water([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1])
```

Output:

```text
6
```

**Example 2**

Input:

```python
trap_water([4, 2, 0, 3, 2, 5])
```

Output:

```text
9
```

### Constraints

- `0 <= len(heights) <= 200000`
- `0 <= heights[i] <= 10**5`

## Explanation

When `left_max < right_max`, the water at `left` is limited by `left_max` no matter what is further right, since a wall at least as tall exists on the right. Symmetrically for the right side.

### Complexity

- Time: O(n). Two pointers; the side with the lower wall is limited by its own running maximum.
- Space: O(1). A few variables.
