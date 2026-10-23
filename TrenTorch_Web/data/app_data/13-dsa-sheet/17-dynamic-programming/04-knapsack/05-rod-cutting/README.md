---
name: sheet-rod-cutting
title: 'Rod Cutting'
tags: [dsa-sheet, dynamic-programming, knapsack]
difficulty: Intermediate
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

## Theory

**Dynamic programming (DP)** solves a problem by combining the answers to smaller versions of the same problem and **remembering** them, so each smaller version is solved only once. It works when the plain recursion keeps asking the same questions (**overlapping subproblems**) and the best answer is built from best answers of smaller parts (**optimal substructure**). The recipe: pick the **state** (what identifies one subproblem), write the **transition** (how a state's answer comes from smaller states), set the **base cases**, and choose the **order**: top-down recursion with a cache, or a bottom-up table. A table often needs only its last row or last few values, which saves memory.

This is an unbounded knapsack where the item "piece of length `k`" weighs `k` and is worth `prices[k - 1]`. **State:** `best(n)`, the best income from a rod of length `n`. **Transition:** the first piece has length `k`: `best(n) = max(prices[k - 1] + best(n - k))` over `k = 1..n`. **Base case:** `best(0) = 0`. `O(length²)`.

## Explanation

`best[n]` is built for increasing `n`, trying each first piece length `k`.
