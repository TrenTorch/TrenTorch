---
name: sheet-zero-one-knapsack
title: '0/1 Knapsack'
tags: [dsa-sheet, dynamic-programming, knapsack]
difficulty: Intermediate
theory: the-0-1-knapsack
---

## Statement

Item `i` weighs `weights[i]` and is worth `values[i]`. The bag holds total weight at most `capacity`. Use each item **at most once**. Return the **largest total value**.

For `weights = [1, 3, 4, 5]`, `values = [1, 4, 5, 7]` and `capacity = 7` the answer is `9` (items of weight 3 and 4).

### Examples

**Example 1**

Input:

```python
knapsack([1, 3, 4, 5], [1, 4, 5, 7], 7)
```

Output:

```text
9
```

**Example 2**

Input:

```python
knapsack([10], [100], 5)
```

Output:

```text
0
```

### Constraints

- `0 <= number of items <= 200`
- `1 <= weights[i] <= 1000`, `0 <= values[i] <= 1000`
- `0 <= capacity <= 10000`

## Explanation

The downward loop over `w` is the whole trick: an upward loop would let the same item be taken many times (the unbounded knapsack).

### Complexity

- Time: O(n * W). Each of the `n` items updates every capacity up to `W` once (pseudo-polynomial; the problem is NP-hard).
- Space: O(W). One row of the table.
