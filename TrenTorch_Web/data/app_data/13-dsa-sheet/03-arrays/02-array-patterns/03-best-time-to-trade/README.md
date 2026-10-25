---
name: sheet-best-time-to-trade
title: 'Best Time to Buy and Sell'
tags: [dsa-sheet, arrays, array-patterns]
difficulty: Beginner
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

## Theory

Trying every buy day and sell day is `O(n²)`. But for a fixed **sell** day, the best buy day is simply the **cheapest price before it**.

So scan once, keeping `lowest`, the minimum price seen so far. On each day the best profit if you sell today is `price - lowest`. Track the maximum of those. Then update `lowest` with today's price.

This "best so far to the left" idea is a close cousin of the running maximum used for leaders and of Kadane's algorithm.

## Explanation

Update the best profit with `price - lowest` **before** lowering `lowest` with today's price, so you never buy and sell on the same day. The profit starts at `0`, so losing trades are ignored.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                    | Variables                  |
| ---------------------------------- | -------------------------- |
| `best = 0`                         | `best = 0`                 |
| `for price in prices:`             | `lowest = None, price = 7` |
| `lowest = price`                   | `lowest = 7`               |
| `lowest = min(lowest, price)`      | `lowest = 1, price = 1`    |
| `best = max(best, price - lowest)` | `best = 4, price = 5`      |
| `for price in prices:`             | `price = 6`                |
| `best = max(best, price - lowest)` | `best = 5`                 |
| `return`                           | `returned = 5`             |

### Complexity

- Time: O(n) where n is the number of elements in prices.
- Extra space: O(1) where no extra dynamic memory is used.
- The brute force takes O(n^2) where n is the number of elements in prices.
