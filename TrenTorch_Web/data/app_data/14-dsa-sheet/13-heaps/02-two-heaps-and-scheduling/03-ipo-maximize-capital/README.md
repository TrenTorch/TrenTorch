---
name: sheet-ipo-maximize-capital
title: 'IPO: Maximize Capital'
tags: [dsa-sheet, heaps, two-heaps-and-scheduling]
difficulty: Advanced
theory: unlock-then-pick-the-best
---

## Statement

You have starting capital `w` and may finish **at most `k` projects**, one after another. Project `i` needs at least `capital[i]` to start, and finishing it gives a **pure profit** of `profits[i]` (added to your capital). Each project can be done once. Return the **largest capital** you can have at the end.

For `k = 2`, `w = 0`, `profits = [1, 2, 3]` and `capital = [0, 1, 1]` the answer is `4`.

### Examples

**Example 1**

Input:

```python
find_maximized_capital(2, 0, [1, 2, 3], [0, 1, 1])
```

Output:

```text
4
```

**Example 2**

Input:

```python
find_maximized_capital(3, 0, [1, 2, 3], [0, 1, 2])
```

Output:

```text
6
```

### Constraints

- `0 <= k <= 100000`
- `0 <= w <= 10**9`
- `0 <= len(profits) == len(capital) <= 100000`
- `0 <= profits[i], capital[i] <= 10**9`

## Explanation

`i` walks through the projects sorted by required capital and pushes every affordable profit into the heap (negated, for a max-heap). Each round takes the best one.

### Complexity

- Time: O(n log n). Sort projects by capital once, then each of at most `k` rounds moves the newly affordable ones to a heap.
- Space: O(n). The sorted list and the heap.
