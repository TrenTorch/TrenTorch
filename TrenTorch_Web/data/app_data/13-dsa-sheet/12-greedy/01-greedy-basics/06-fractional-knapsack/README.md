---
name: sheet-fractional-knapsack
title: 'Fractional Knapsack'
tags: [dsa-sheet, greedy, greedy-basics]
difficulty: Intermediate
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

## Theory

A **greedy** algorithm builds the answer step by step and, at each step, takes the choice that looks best **right now**, without ever going back. It is fast and simple, but it is only correct when the problem has a structure that makes local choices safe. The hard part is the **proof**: show that the greedy choice can always be part of some best answer.

When you can take fractions, the best use of limited capacity is to fill it with the items that give the **most value per unit of weight**. Sort the items by `value / weight` from the highest. Take each whole item while it fits; for the first one that does not fit, take the **fraction** that fills the bag, and stop.

Greedy is correct here because every unit of weight can be spent independently, so you always want the best price per unit. The version where items are all-or-nothing (0/1 knapsack) breaks this argument and needs dynamic programming.

## Explanation

`key` sorts by value per weight in decreasing order. `take = min(weight, capacity)` is the part of the item that fits; its value is `value * take / weight`.
