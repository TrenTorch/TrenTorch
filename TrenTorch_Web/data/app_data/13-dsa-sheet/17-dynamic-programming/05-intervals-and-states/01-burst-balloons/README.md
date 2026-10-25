---
name: sheet-burst-balloons
title: 'Burst Balloons'
tags: [dsa-sheet, dynamic-programming, intervals-and-states]
difficulty: Mastery
---

## Statement

There are balloons with numbers `nums[i]`. Bursting balloon `i` gives `nums[i - 1] * nums[i] * nums[i + 1]` coins, where `i - 1` and `i + 1` are the **neighbours that are still there** (a missing neighbour counts as a balloon with number 1). Burst all balloons in the best order and return the **maximum coins**.

For `[3, 1, 5, 8]` the answer is `167`.

The starter code tries every order. It is correct but too slow for more than a few balloons.

### Examples

**Example 1**

Input:

```python
max_coins([3, 1, 5, 8])
```

Output:

```text
167
```

**Explanation:** Optimal order bursts 5, then 3, then 8, then 1 yielding 167 coins.

**Example 2**

Input:

```python
max_coins([1, 5])
```

Output:

```text
10
```

**Explanation:** Bursting balloon 1 first then balloon 5 gives 10 coins.

### Constraints

- `0 <= len(nums) <= 120`
- `0 <= nums[i] <= 100`

## Theory

**Dynamic programming (DP)** solves a problem by combining the answers to smaller versions of the same problem and **remembering** them, so each smaller version is solved only once. It works when the plain recursion keeps asking the same questions (**overlapping subproblems**) and the best answer is built from best answers of smaller parts (**optimal substructure**). The recipe: pick the **state** (what identifies one subproblem), write the **transition** (how a state's answer comes from smaller states), set the **base cases**, and choose the **order**: top-down recursion with a cache, or a bottom-up table. A table often needs only its last row or last few values, which saves memory.

The obvious state ("which balloons are left") has `2^n` values. The trick: think about which balloon is burst **last** in a range. If balloon `k` is the last one burst in the range `(i, j)` (exclusive), its neighbours at that moment are exactly the borders `i` and `j`, and the two sides `(i, k)` and `(k, j)` are independent problems.

**State:** `best(i, j)`, the most coins from balloons strictly between `i` and `j`. **Transition:** `best(i, j) = max over k of best(i, k) + best(k, j) + nums[i] * nums[k] * nums[j]`. Pad `nums` with a `1` at both ends. **Order:** by increasing range length. `O(n³)`.

This "choose the last one" idea is the standard interval DP.

## Explanation

`dp[i][j]` is filled for increasing `j - i`. `k` runs over the balloons between the borders.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                                    | Variables                                                                                                                        |
| -------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| `a = [1] + nums + [1]`                             | `a = [1, 3, 1, 5, 8, 1]`                                                                                                         |
| `for k in range(i + 1, j):`                        | `n = 6, dp = [[0, 0, 3, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, ..., length = 2, i = 1, j = 3, best = 0, k = 2, value = 3` |
| `best = 0`                                         | `dp = [[0, 0, 3, 0, 0, 0], [0, 0, 0, 15, 0, 0], [0, 0, 0, 0, 40..., i = 3, j = 5, k = 3, value = 40`                             |
| `j = i + length`                                   | `dp = [[0, 0, 3, 30, 0, 0], [0, 0, 0, 15, 0, 0], [0, 0, 0, 0, 4..., length = 3, i = 1, j = 4, best = 30, k = 2, value = 8`       |
| `value = dp[i][k] + dp[k][j] + a[i] * a[k] * a[j]` | `dp = [[0, 0, 3, 30, 0, 0], [0, 0, 0, 15, 135, 0], [0, 0, 0, 0,..., i = 2, j = 5, best = 45, k = 4, value = 48`                  |
| `for i in range(n - length):`                      | `dp = [[0, 0, 3, 30, 159, 0], [0, 0, 0, 15, 135, 0], [0, 0, 0, ..., length = 4, i = 1, j = 4, best = 159, k = 3, value = 70`     |
| `for length in range(2, n):`                       | `dp = [[0, 0, 3, 30, 159, 0], [0, 0, 0, 15, 135, 159], [0, 0, 0..., length = 5, j = 5, k = 4, value = 159`                       |
| `return`                                           | `returned = 167`                                                                                                                 |

### Complexity

- Time: O(n^3).
- Extra space: O(n^2).
- The brute force takes O(n! * n).
