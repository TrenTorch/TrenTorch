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

**Explanation:** The best rectangle spans the two middle bars of height 5 and 6, using minimum height 5 over width 2 for area 10, which is larger than any other span.

**Example 2**

Input:

```python
largest_rectangle([2, 4])
```

Output:

```text
4
```

**Explanation:** With heights 2 and 4, the widest rectangle using both bars has height 2 over width 2 for area 4, equal to the single bar of height 4 over width 1.

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

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                         | Variables                                                    |
| --------------------------------------- | ------------------------------------------------------------ |
| `best = 0`                              | `best = 0`                                                   |
| `for i, h in enumerate(heights + [0]):` | `stack = [0], i = 1, h = 1`                                  |
| `for i, h in enumerate(heights + [0]):` | `best = 2, stack = [1], i = 2, h = 5, height = 2, left = -1` |
| `for i, h in enumerate(heights + [0]):` | `stack = [1, 2, 3], i = 4, h = 2`                            |
| `left = stack[-1] if stack else -1`     | `best = 6, stack = [1], height = 5, left = 1`                |
| `stack.append(i)`                       | `best = 10, stack = [1, 4, 5], i = 5, h = 3`                 |
| `left = stack[-1] if stack else -1`     | `stack = [1], i = 6, h = 0, height = 2`                      |
| `return`                                | `returned = 10`                                              |

### Complexity

- Time: O(n) where n is number of bars.
- Extra space: O(n) where n is number of bars.
- The brute force takes O(n^2) where n is number of bars.
