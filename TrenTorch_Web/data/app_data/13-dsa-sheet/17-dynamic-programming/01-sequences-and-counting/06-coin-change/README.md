---
name: sheet-coin-change
title: 'Coin Change'
tags: [dsa-sheet, dynamic-programming, sequences-and-counting]
difficulty: Intermediate
---

## Statement

`coins` lists coin values (you may use each value any number of times). Return the **fewest coins** that add up to `amount`, or `-1` if it is impossible.

For `coins = [1, 2, 5]` and `amount = 11` the answer is `3` (`5 + 5 + 1`).

The starter code is a plain recursion. It is correct but too slow for large amounts.

### Examples

**Example 1**

Input:

```python
coin_change([1, 2, 5], 11)
```

Output:

```text
3
```

**Example 2**

Input:

```python
coin_change([2], 3)
```

Output:

```text
-1
```

### Constraints

- `0 <= len(coins) <= 12`
- `1 <= coins[i] <= 10000`
- `0 <= amount <= 10000`

## Theory

**Dynamic programming (DP)** solves a problem by combining the answers to smaller versions of the same problem and **remembering** them, so each smaller version is solved only once. It works when the plain recursion keeps asking the same questions (**overlapping subproblems**) and the best answer is built from best answers of smaller parts (**optimal substructure**). The recipe: pick the **state** (what identifies one subproblem), write the **transition** (how a state's answer comes from smaller states), set the **base cases**, and choose the **order**: top-down recursion with a cache, or a bottom-up table. A table often needs only its last row or last few values, which saves memory.

A greedy choice (take the largest coin) can fail: with coins `[1, 3, 4]` and amount `6`, greedy gives `4 + 1 + 1` (3 coins) but `3 + 3` needs 2.

**State:** `fewest(a)`, the fewest coins for amount `a`. **Transition:** the last coin is some `c <= a`: `fewest(a) = 1 + min(fewest(a - c))` over all coins. **Base case:** `fewest(0) = 0`; unreachable amounts are `infinity`. Fill `a = 1..amount` in order. `O(amount × coins)`.

The plain recursion recomputes `fewest(a - c)` for the same `a - c` along many different coin orders: exponential time.

## Explanation

`best[a]` is the answer for amount `a`; `inf` marks unreachable. The final `inf` becomes `-1`.
