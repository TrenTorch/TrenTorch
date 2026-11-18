---
name: sheet-best-time-to-trade
title: 'Best Time to Buy and Sell'
tags: [dsa-sheet, arrays, array-patterns]
difficulty: Beginner
theory: remembering-the-best-so-far
---

## Statement

`prices[i]` is the price of a stock on day `i`. You may buy on one day and sell on a **later** day, once. Return the largest profit you can make, or `0` if every possible trade loses money (or there are fewer than two days).

The starter code tries every pair of days. It is correct but too slow for long lists. Make it fast.

### Examples

**Example 1**

Input:

```python
stock_best_profit([7, 1, 5, 3, 6, 4])
```

Output:

```text
5
```

Buy at 1, sell at 6 for a profit of 5.

**Example 2**

Input:

```python
stock_best_profit([7, 6, 4, 3, 1])
```

Output:

```text
0
```

The price only falls, so the best is not to trade: 0.

### Constraints

- `0 <= len(prices) <= 2 * 10**5`
- `0 <= prices[i] <= 10**9`

## Explanation

Update the best profit with `price - lowest` **before** lowering `lowest` with today's price, so you never buy and sell on the same day. The profit starts at `0`, so losing trades are ignored.

### Complexity

- Time: O(n). One pass keeping the lowest price so far.
- Space: O(1). Two numbers.
