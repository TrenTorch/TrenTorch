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

**Explanation:** Take item weight 10 value 60 and item weight 20 value 100 using 30 weight out of capacity 50, then take 20/30 of item weight 30 value 120 proportionally reaching total 240.0

**Example 2**

Input:

```python
fractional_knapsack([[500, 30]], 10)
```

Output:

```text
166.66666666666666
```

**Explanation:** Only item weight 30 value 500 with capacity 10 takes 10/30 proportion yielding output 166.66666666666666

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

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                                                                   | Variables                                 |
| --------------------------------------------------------------------------------- | ----------------------------------------- |
| `total = 0.0`                                                                     | `total = 0.0`                             |
| `take = min(weight, capacity)`                                                    | `value = 60, weight = 10, take = 10`      |
| `total += value * take / weight`                                                  | `total = 60.0`                            |
| `for value, weight in sorted(items, key=lambda it: it[0] / it[1], reverse=True):` | `capacity = 40, value = 100, weight = 20` |
| `total += value * take / weight`                                                  | `total = 160.0, take = 20`                |
| `for value, weight in sorted(items, key=lambda it: it[0] / it[1], reverse=True):` | `capacity = 20, value = 120, weight = 30` |
| `total += value * take / weight`                                                  | `total = 240.0`                           |
| `return`                                                                          | `returned = 240.0`                        |

### Complexity

- Time: O(n log n) n items q capacity.
- Extra space: O(n) n items extra list.
- The brute force takes O(2^n * n) where n is the number of items; there are 2^n subsets, and checking each takes O(n).
