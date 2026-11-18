---
name: sheet-container-with-most-water
title: 'Container With Most Water'
tags: [dsa-sheet, two-pointers, two-pointers]
difficulty: Intermediate
theory: the-widest-container
---

## Statement

`heights[i]` is the height of a vertical line at position `i`. Choose **two lines** that, together with the x-axis, form a container, and return the **largest amount of water** it can hold: `min(height of the two lines) * distance between them`. The container cannot be tilted.

For `[1, 8, 6, 2, 5, 4, 8, 3, 7]` the answer is `49`.

The starter code tries every pair. It is correct but too slow for many lines.

### Examples

**Example 1**

Input:

```python
max_water([1, 8, 6, 2, 5, 4, 8, 3, 7])
```

Output:

```text
49
```

**Example 2**

Input:

```python
max_water([1, 1])
```

Output:

```text
1
```

### Constraints

- `0 <= len(heights) <= 200000`
- `0 <= heights[i] <= 10**4`

## Explanation

Each step computes the area of the current pair and moves the pointer at the shorter line, since keeping it could only give smaller or equal areas.

### Complexity

- Time: O(n). Two pointers; the shorter wall can never do better with a smaller width, so it is the one that moves.
- Space: O(1). A few variables.
