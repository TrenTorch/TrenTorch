---
name: sheet-stock-with-k-transactions
title: 'Stock Trading With at Most K Transactions'
tags: [dsa-sheet, dynamic-programming, intervals-and-states]
difficulty: Mastery
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

**Explanation:** The maximum profit of 7 is achieved by buying at 2 and selling at 6, then buying at 0 and selling at 3.

**Example 2**

Input:

```python
max_profit_k(1, [7, 6, 4, 3, 1])
```

Output:

```text
0
```

**Explanation:** No profit can be made because the prices are always decreasing.

### Constraints

- `0 <= k <= 100`
- `0 <= len(prices) <= 4000`
- `0 <= prices[i] <= 1000`

## Theory

**Dynamic programming (DP)** solves a problem by combining the answers to smaller versions of the same problem and **remembering** them, so each smaller version is solved only once. It works when the plain recursion keeps asking the same questions (**overlapping subproblems**) and the best answer is built from best answers of smaller parts (**optimal substructure**). The recipe: pick the **state** (what identifies one subproblem), write the **transition** (how a state's answer comes from smaller states), set the **base cases**, and choose the **order**: top-down recursion with a cache, or a bottom-up table. A table often needs only its last row or last few values, which saves memory.

**State:** after each day, for each number of transactions `t`: `hold[t]` (the best profit while holding a share bought as the `t`-th transaction) and `free[t]` (the best profit after completing `t` transactions, not holding). **Transition** for a price `p`: `hold[t] = max(hold[t], free[t - 1] - p)` and `free[t] = max(free[t], hold[t] + p)`.

Updating `t` from high to low (or computing `hold` first) keeps a buy and a sell on the same day from counting as two transactions. `O(n × k)`. When `k >= n / 2` the limit is irrelevant and the answer is the sum of all positive differences.

## Explanation

`hold[t]` starts at minus infinity (nothing bought yet). Each day relaxes both arrays for every `t`; `free[k]` is the answer.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                           | Variables                                                 |
| ----------------------------------------- | --------------------------------------------------------- |
| `hold = [float("-inf")] * (k + 1)`        | `hold = [-inf, -inf, -inf]`                               |
| `hold[t] = max(hold[t], free[t - 1] - p)` | `hold = [-inf, -3, -inf], free = [0, 0, 0], p = 3, t = 1` |
| `hold[t] = max(hold[t], free[t - 1] - p)` | `hold = [-inf, -2, -3], p = 2`                            |
| `for t in range(1, k + 1):`               | `hold = [-inf, -2, -2], p = 6`                            |
| `for p in prices:`                        | `free = [0, 4, 4], p = 5, t = 2`                          |
| `for p in prices:`                        | `hold = [-inf, -2, -1], p = 0`                            |
| `for p in prices:`                        | `hold = [-inf, 0, 4], p = 3`                              |
| `return`                                  | `returned = 7`                                            |

### Complexity

- Time: O(n*k).
- Extra space: O(k).
- The brute force takes O(n*k).
