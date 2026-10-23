---
name: sheet-min-cost-climbing-stairs
title: 'Min Cost Climbing Stairs'
tags: [dsa-sheet, dynamic-programming, sequences-and-counting]
difficulty: Beginner
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

## Theory

**Dynamic programming (DP)** solves a problem by combining the answers to smaller versions of the same problem and **remembering** them, so each smaller version is solved only once. It works when the plain recursion keeps asking the same questions (**overlapping subproblems**) and the best answer is built from best answers of smaller parts (**optimal substructure**). The recipe: pick the **state** (what identifies one subproblem), write the **transition** (how a state's answer comes from smaller states), set the **base cases**, and choose the **order**: top-down recursion with a cache, or a bottom-up table. A table often needs only its last row or last few values, which saves memory.

**State:** `best(i)`, the cheapest cost to be standing on stair `i` (before paying for it). **Transition:** you arrive from stair `i - 1` (paying `cost[i - 1]`) or from `i - 2` (paying `cost[i - 2]`): `best(i) = min(best(i - 1) + cost[i - 1], best(i - 2) + cost[i - 2])`. **Base cases:** `best(0) = best(1) = 0`. **Answer:** `best(n)`, where `n = len(cost)` is the top.

Only the last two values are needed. `O(n)`.

## Explanation

`prev2` and `prev1` hold `best(i - 2)` and `best(i - 1)`; the loop computes `best(i)` for `i` up to the top.
