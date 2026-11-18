---
name: sheet-unbounded-knapsack
title: 'Unbounded Knapsack'
tags: [dsa-sheet, dynamic-programming, knapsack]
difficulty: Intermediate
theory: the-unbounded-knapsack
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

## Explanation

The upward loop over `w` reuses the freshly updated `best[w - weight]`, which is exactly "take the item again".

### Complexity

- Time: O(n * W). Each of the `n` items updates every capacity up to `W` once (pseudo-polynomial).
- Space: O(W). One row of the table.
