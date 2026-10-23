---
name: sheet-best-time-to-trade-ii
title: 'Buy and Sell Stock, Many Trades'
tags: [dsa-sheet, greedy, greedy-basics]
difficulty: Beginner
---

## Statement

`prices[i]` is a stock price on day `i`. You may buy and sell as many times as you like, but you can hold **at most one share** at a time (sell before you buy again, on the same day is allowed). Return the **maximum total profit**.

For `[7, 1, 5, 3, 6, 4]` the answer is `7` (buy at 1, sell at 5; buy at 3, sell at 6).

### Examples

**Example 1**

Input:

```python
max_profit_many([7, 1, 5, 3, 6, 4])
```

Output:

```text
7
```

**Example 2**

Input:

```python
max_profit_many([7, 6, 4, 3, 1])
```

Output:

```text
0
```

### Constraints

- `0 <= len(prices) <= 200000`
- `0 <= prices[i] <= 10**9`

## Theory

A **greedy** algorithm builds the answer step by step and, at each step, takes the choice that looks best **right now**, without ever going back. It is fast and simple, but it is only correct when the problem has a structure that makes local choices safe. The hard part is the **proof**: show that the greedy choice can always be part of some best answer.

Any rise over several days is the sum of the one-day rises: `price[3] - price[0] = (p1 - p0) + (p2 - p1) + (p3 - p2)`. So collecting every **positive day-to-day difference** collects every profitable trade, and skipping the negative ones avoids every loss.

The greedy rule: add `max(0, prices[i] - prices[i - 1])` for every day. `O(n)`, one pass.

## Explanation

Every upward step is profit you could have captured by buying the day before and selling today. A downward step is never taken.
