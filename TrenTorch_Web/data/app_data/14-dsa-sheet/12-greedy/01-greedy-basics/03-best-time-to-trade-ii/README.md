---
name: sheet-best-time-to-trade-ii
title: 'Buy and Sell Stock, Many Trades'
tags: [dsa-sheet, greedy, greedy-basics]
difficulty: Beginner
theory: take-every-rise
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

## Explanation

Every upward step is profit you could have captured by buying the day before and selling today. A downward step is never taken.

### Complexity

- Time: O(n). One pass adding every rise between neighbouring days.
- Space: O(1). A running sum.
