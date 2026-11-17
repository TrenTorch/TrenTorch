---
name: sheet-min-cost-climbing-stairs
title: 'Min Cost Climbing Stairs'
tags: [dsa-sheet, dynamic-programming, sequences-and-counting]
difficulty: Beginner
theory: climbing-stairs
---

## Statement

`cost[i]` is the price to **step off stair `i`**; after paying you may climb **1 or 2** stairs. You may **start on stair 0 or stair 1**. The top is one step beyond the last stair. Return the **minimum total cost** to reach the top.

For `[10, 15, 20]` the answer is `15` (start on stair 1, pay 15, jump 2 to the top).

### Examples

**Example 1**

Input:

```python
min_cost_climbing([10, 15, 20])
```

Output:

```text
15
```

**Example 2**

Input:

```python
min_cost_climbing([1, 100, 1, 1, 1, 100, 1, 1, 100, 1])
```

Output:

```text
6
```

### Constraints

- `0 <= len(cost) <= 1000000`
- `0 <= cost[i] <= 999`

## Explanation

`prev2` and `prev1` hold `best(i - 2)` and `best(i - 1)`; the loop computes `best(i)` for `i` up to the top.

### Complexity

- Time: O(n). One pass; each step only needs the best costs of the two steps before it.
- Space: O(1). Two numbers.
