---
name: sheet-ipo-maximize-capital
title: 'IPO: Maximize Capital'
tags: [dsa-sheet, heaps, two-heaps-and-scheduling]
difficulty: Advanced
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

## Theory

A **heap** (priority queue) always gives you the **smallest** item in `O(log n)`, while letting you add items in `O(log n)`. Python's `heapq` module implements a **min-heap** on a plain list: `heappush(h, x)`, `heappop(h)` (the smallest), `h[0]` (peek) and `heapify(h)` (turn a list into a heap in `O(n)`). For a **max-heap** push the negated values.

At each step, among all projects you can **afford** (`capital[i] <= current capital`), do the one with the **largest profit**: more capital now never hurts, and it can only unlock more projects.

Two structures work together: sort the projects by the capital they need; as your capital grows, move all newly affordable projects into a **max-heap of profits**. Pop the best one, add its profit, and repeat up to `k` times. If the heap is empty (nothing affordable), stop.

`O(n log n)`.

## Explanation

`i` walks through the projects sorted by required capital and pushes every affordable profit into the heap (negated, for a max-heap). Each round takes the best one.
