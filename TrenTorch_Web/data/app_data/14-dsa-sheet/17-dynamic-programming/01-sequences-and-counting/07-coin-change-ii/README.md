---
name: sheet-coin-change-ii
title: 'Coin Change: Count the Ways'
tags: [dsa-sheet, dynamic-programming, sequences-and-counting]
difficulty: Intermediate
theory: coin-change
---

## Statement

`coins` are the coin values, each available without limit. Return the **number of different combinations** of coins that add up to `amount` (the order does not matter: `1+2` and `2+1` are the same). Return the answer modulo `10**9 + 7`.

For `amount = 5` and `coins = [1, 2, 5]` the answer is `4`.

### Examples

**Example 1**

Input:

```python
count_change(5, [1, 2, 5])
```

Output:

```text
4
```

**Example 2**

Input:

```python
count_change(3, [2])
```

Output:

```text
0
```

### Constraints

- `0 <= len(coins) <= 100`
- `1 <= coins[i] <= 5000`, all different
- `0 <= amount <= 100000`

## Explanation

Processing one coin at a time guarantees every combination is built in one fixed order of coins, so it is counted once.

### Complexity

- Time: O(amount * k). For each of the `k` coins, update every amount up to the target once.
- Space: O(amount). The table of counts.
