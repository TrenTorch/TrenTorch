---
name: sheet-coin-change
title: 'Coin Change'
tags: [dsa-sheet, dynamic-programming, sequences-and-counting]
difficulty: Intermediate
theory: coin-change
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

## Explanation

`best[a]` is the answer for amount `a`; `inf` marks unreachable. The final `inf` becomes `-1`.

### Complexity

- Time: O(amount * k). For each amount up to the target, try each of the `k` coins.
- Space: O(amount). The table of best counts.
