---
name: sheet-stock-with-cooldown
title: 'Stock Trading With Cooldown'
tags: [dsa-sheet, dynamic-programming, intervals-and-states]
difficulty: Advanced
theory: state-machines-stock-problems
---

## Statement

`prices[i]` is a stock price on day `i`. You may trade as often as you like but hold at most one share, and after you **sell** you cannot buy on the **next day** (cooldown of one day). Return the **maximum profit**.

For `[1, 2, 3, 0, 2]` the answer is `3` (buy at 1, sell at 2, cool down, buy at 0, sell at 2).

The starter code tries every action on every day. It is correct but too slow for many days.

### Examples

**Example 1**

Input:

```python
max_profit_cooldown([1, 2, 3, 0, 2])
```

Output:

```text
3
```

**Example 2**

Input:

```python
max_profit_cooldown([1])
```

Output:

```text
0
```

### Constraints

- `0 <= len(prices) <= 300000`
- `0 <= prices[i] <= 1000`

## Explanation

The three variables are updated at the same time from the previous day's values (the tuple assignment evaluates the right side first).

### Complexity

- Time: O(n). One pass with three states.
- Space: O(1). Three numbers.
