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

**Example 2**

Input:

```python
max_coins([1, 5])
```

Output:

```text
10
```

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
