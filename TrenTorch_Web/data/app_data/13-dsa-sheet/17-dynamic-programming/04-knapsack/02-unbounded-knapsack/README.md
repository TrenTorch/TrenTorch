---
name: sheet-unbounded-knapsack
title: 'Unbounded Knapsack'
tags: [dsa-sheet, dynamic-programming, knapsack]
difficulty: Intermediate
---

## Statement

Item `i` weighs `weights[i]` and is worth `values[i]`; you may take **each item any number of times**. The bag holds total weight at most `capacity`. Return the **largest total value**.

For `weights = [1, 3, 4]`, `values = [15, 50, 60]` and `capacity = 8` the answer is `130` (two items of weight 3 and two of weight 1).

### Examples

**Example 1**

Input:

```python
unbounded_knapsack([1, 3, 4], [15, 50, 60], 8)
```

Output:

```text
130
```

**Example 2**

Input:

```python
unbounded_knapsack([5], [10], 4)
```

Output:

```text
0
```

### Constraints

- `0 <= number of items <= 100`
- `1 <= weights[i] <= 1000`, `0 <= values[i] <= 1000`
- `0 <= capacity <= 20000`

## Theory

**Dynamic programming (DP)** solves a problem by combining the answers to smaller versions of the same problem and **remembering** them, so each smaller version is solved only once. It works when the plain recursion keeps asking the same questions (**overlapping subproblems**) and the best answer is built from best answers of smaller parts (**optimal substructure**). The recipe: pick the **state** (what identifies one subproblem), write the **transition** (how a state's answer comes from smaller states), set the **base cases**, and choose the **order**: top-down recursion with a cache, or a bottom-up table. A table often needs only its last row or last few values, which saves memory.

Compare with the 0/1 knapsack: now an item can be taken again after being taken, so the update loop over the capacity goes **upwards**. **State:** `best[w]`, the best value with room `w`. **Transition:** `best[w] = max(best[w], best[w - weight] + value)` for each item; since `best[w - weight]` may already include the same item, repeated use is allowed. **Base case:** `best[0] = 0`.

The difference between the two problems is only the direction of one loop. `O(items × capacity)`.

## Explanation

The upward loop over `w` reuses the freshly updated `best[w - weight]`, which is exactly "take the item again".
