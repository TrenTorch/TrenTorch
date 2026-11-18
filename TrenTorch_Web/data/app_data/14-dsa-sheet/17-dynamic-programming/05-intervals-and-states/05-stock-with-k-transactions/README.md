---
name: sheet-stock-with-k-transactions
title: 'Stock Trading With at Most K Transactions'
tags: [dsa-sheet, dynamic-programming, intervals-and-states]
difficulty: Mastery
theory: state-machines-stock-problems
---

## Statement

`prices[i]` is a stock price on day `i`. You may complete **at most `k` transactions** (a buy followed by a sell), holding at most one share at a time. Return the **maximum profit**.

For `k = 2` and `prices = [3, 2, 6, 5, 0, 3]` the answer is `7` (buy 2, sell 6, buy 0, sell 3).

The starter code tries every action on every day. It is correct but too slow for many days.

### Examples

**Example 1**

Input:

```python
max_profit_k(2, [3, 2, 6, 5, 0, 3])
```

Output:

```text
7
```

**Example 2**

Input:

```python
max_profit_k(1, [7, 6, 4, 3, 1])
```

Output:

```text
0
```

### Constraints

- `0 <= k <= 100`
- `0 <= len(prices) <= 4000`
- `0 <= prices[i] <= 1000`

## Explanation

`hold[t]` starts at minus infinity (nothing bought yet). Each day relaxes both arrays for every `t`; `free[k]` is the answer.

### Complexity

- Time: O(n * k). For each day, update the `k` transaction levels (if `k >= n / 2` it is the unlimited case, O(n)).
- Space: O(k). Two arrays of `k + 1` numbers.
