---
name: sheet-coin-change-ii
title: 'Coin Change: Count the Ways'
tags: [dsa-sheet, dynamic-programming, sequences-and-counting]
difficulty: Intermediate
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

## Theory

**Dynamic programming (DP)** solves a problem by combining the answers to smaller versions of the same problem and **remembering** them, so each smaller version is solved only once. It works when the plain recursion keeps asking the same questions (**overlapping subproblems**) and the best answer is built from best answers of smaller parts (**optimal substructure**). The recipe: pick the **state** (what identifies one subproblem), write the **transition** (how a state's answer comes from smaller states), set the **base cases**, and choose the **order**: top-down recursion with a cache, or a bottom-up table. A table often needs only its last row or last few values, which saves memory.

Counting **combinations** (not orders) needs care. If you loop over the amounts first and then the coins, `1+2` and `2+1` are counted separately (that counts sequences). To count each combination once, make the **coins the outer loop**: for each coin `c`, and for each amount `a` from `c` upwards, `ways[a] += ways[a - c]`.

After handling coin `c`, `ways[a]` is the number of combinations using only the coins seen so far. Starting with `ways[0] = 1` (one way to make 0: take nothing). `O(amount × coins)` time and `O(amount)` memory.

## Explanation

Processing one coin at a time guarantees every combination is built in one fixed order of coins, so it is counted once.
