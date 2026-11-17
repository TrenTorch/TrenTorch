---
name: sheet-largest-rectangle-histogram
title: 'Largest Rectangle in a Histogram'
tags: [dsa-sheet, stack-and-queue, monotonic-stack]
difficulty: Advanced
theory: the-largest-rectangle-in-a-histogram
---

## Statement

`heights[i]` is the height of bar `i` in a histogram; every bar is 1 wide and the bars touch. Return the **area of the largest rectangle** that fits inside the histogram.

For `[2, 1, 5, 6, 2, 3]` the answer is `10` (the bars of height 5 and 6 make a rectangle of height 5 and width 2).

The starter code tries every pair of bars. It is correct but too slow for long histograms.

### Examples

**Example 1**

Input:

```python
largest_rectangle([2, 1, 5, 6, 2, 3])
```

Output:

```text
10
```

**Example 2**

Input:

```python
largest_rectangle([2, 4])
```

Output:

```text
4
```

### Constraints

- `0 <= len(heights) <= 200000`
- `0 <= heights[i] <= 10**9`

## Explanation

When bar `top` is popped by bar `i`, the stack below it holds the nearest shorter bar on the left. The width is the gap between that bar and `i`. The sentinel `0` forces all remaining bars to be popped.

### Complexity

- Time: O(n). Each bar is pushed once and popped at most once, and the area is finished when the bar is popped.
- Space: O(n). The stack.
