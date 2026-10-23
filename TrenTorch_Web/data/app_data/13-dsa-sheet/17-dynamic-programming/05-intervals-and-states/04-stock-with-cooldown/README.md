---
name: sheet-stock-with-cooldown
title: 'Stock Trading With Cooldown'
tags: [dsa-sheet, dynamic-programming, intervals-and-states]
difficulty: Advanced
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

## Theory

**Dynamic programming (DP)** solves a problem by combining the answers to smaller versions of the same problem and **remembering** them, so each smaller version is solved only once. It works when the plain recursion keeps asking the same questions (**overlapping subproblems**) and the best answer is built from best answers of smaller parts (**optimal substructure**). The recipe: pick the **state** (what identifies one subproblem), write the **transition** (how a state's answer comes from smaller states), set the **base cases**, and choose the **order**: top-down recursion with a cache, or a bottom-up table. A table often needs only its last row or last few values, which saves memory.

A day can end in one of three **states**: holding a share (`hold`), just sold (`sold`, in cooldown), or resting with no share (`rest`, free to buy). The state machine for each day:

- `hold = max(hold, rest - price)` (keep holding, or buy from a resting state),
- `sold = hold_before + price` (sell what you held),
- `rest = max(rest, sold_before)` (stay free, or come out of the cooldown).

The answer is `max(sold, rest)` on the last day. Writing a problem as a **finite state machine** and updating all states each day is a very common DP style. `O(n)` time, `O(1)` memory.

## Explanation

The three variables are updated at the same time from the previous day's values (the tuple assignment evaluates the right side first).
