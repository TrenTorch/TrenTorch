---
name: sheet-largest-rectangle-histogram
title: 'Largest Rectangle in a Histogram'
tags: [dsa-sheet, stack-and-queue, monotonic-stack]
difficulty: Advanced
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

## Theory

A **stack** is last in, first out: you only add (`push`) and remove (`pop`) at the top. In Python a list does this with `append()` and `pop()`, both `O(1)`.

Fix a bar as the **shortest bar** of the rectangle. The rectangle can stretch left and right until it meets a shorter bar, so its width is `right_smaller - left_smaller - 1` and its area is `height * width`. The answer is the best over all bars.

A monotonic stack finds both borders at once. Keep indices of bars with **increasing heights**. When a new bar `i` is shorter than the top bar, the top bar can stretch no further to the right: **pop** it, its right border is `i`, and its left border is the new top of the stack (or the start, if the stack is empty). Compute its area right then.

Add a bar of height `0` at the end to flush everything. `O(n)` time because each bar is pushed and popped once.

## Explanation

When bar `top` is popped by bar `i`, the stack below it holds the nearest shorter bar on the left. The width is the gap between that bar and `i`. The sentinel `0` forces all remaining bars to be popped.
