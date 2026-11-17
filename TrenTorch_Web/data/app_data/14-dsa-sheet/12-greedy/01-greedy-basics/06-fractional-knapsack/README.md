---
name: sheet-fractional-knapsack
title: 'Fractional Knapsack'
tags: [dsa-sheet, greedy, greedy-basics]
difficulty: Intermediate
theory: best-value-per-kilogram
---

## Statement

Each item is a pair `[value, weight]`. A bag holds total weight at most `capacity`. You may take **a fraction of an item** (half the weight gives half the value). Return the **largest total value** you can carry, as a number (answers within `1e-9` are accepted).

For `items = [[60, 10], [100, 20], [120, 30]]` and `capacity = 50` the answer is `240.0`.

### Examples

**Example 1**

Input:

```python
fractional_knapsack([[60, 10], [100, 20], [120, 30]], 50)
```

Output:

```text
240.0
```

**Example 2**

Input:

```python
fractional_knapsack([[500, 30]], 10)
```

Output:

```text
166.66666666666666
```

### Constraints

- `0 <= len(items) <= 200000`
- `1 <= value, weight <= 1000`
- `0 <= capacity <= 10**6`

## Explanation

`key` sorts by value per weight in decreasing order. `take = min(weight, capacity)` is the part of the item that fits; its value is `value * take / weight`.

### Complexity

- Time: O(n log n). Sorting by value per weight dominates; filling the bag is one pass. (A selection algorithm can reach O(n) on average, but sorting is the standard method).
- Space: O(n). The sorted list.
