---
name: sheet-rod-cutting
title: 'Rod Cutting'
tags: [dsa-sheet, dynamic-programming, knapsack]
difficulty: Intermediate
theory: counting-versions-and-two-budgets
---

## Statement

A rod has integer length `length`. `prices[i]` is the price of a piece of length `i + 1`. You may cut the rod into pieces of integer lengths (or not cut at all). Return the **largest total price**. The length is at most `len(prices)`.

For `prices = [1, 5, 8, 9, 10, 17, 17, 20]` and `length = 8` the answer is `22` (pieces of length 2 and 6).

### Examples

**Example 1**

Input:

```python
rod_cutting([1, 5, 8, 9, 10, 17, 17, 20], 8)
```

Output:

```text
22
```

**Example 2**

Input:

```python
rod_cutting([3, 5, 8, 9, 10, 17, 17, 20], 8)
```

Output:

```text
24
```

### Constraints

- `0 <= length <= len(prices) <= 2000`
- `0 <= prices[i] <= 10000`

## Explanation

`best[n]` is built for increasing `n`, trying each first piece length `k`.

### Complexity

- Time: O(n^2). For each length up to `n`, try every first cut.
- Space: O(n). The table of best prices.
