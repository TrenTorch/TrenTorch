---
name: sheet-target-sum
title: 'Target Sum'
tags: [dsa-sheet, dynamic-programming, sequences-and-counting]
difficulty: Intermediate
---

## Statement

Put a `+` or a `-` in front of **every** number of `nums`. Return the **number of ways** to make the total equal `target`.

For `nums = [1, 1, 1, 1, 1]` and `target = 3` the answer is `5`.

### Examples

**Example 1**

Input:

```python
find_target_sum_ways([1, 1, 1, 1, 1], 3)
```

Output:

```text
5
```

**Example 2**

Input:

```python
find_target_sum_ways([1], 1)
```

Output:

```text
1
```

### Constraints

- `0 <= len(nums) <= 100`
- `0 <= nums[i] <= 100`
- `-10**4 <= target <= 10**4`

## Theory

**Dynamic programming (DP)** solves a problem by combining the answers to smaller versions of the same problem and **remembering** them, so each smaller version is solved only once. It works when the plain recursion keeps asking the same questions (**overlapping subproblems**) and the best answer is built from best answers of smaller parts (**optimal substructure**). The recipe: pick the **state** (what identifies one subproblem), write the **transition** (how a state's answer comes from smaller states), set the **base cases**, and choose the **order**: top-down recursion with a cache, or a bottom-up table. A table often needs only its last row or last few values, which saves memory.

**State:** the sum so far after the first `i` numbers. **Transition:** each number is added or subtracted. Instead of a table indexed by sum (which may be negative), keep a **dictionary** `ways[sum] -> count` for the numbers processed so far; each new number `x` makes a new dictionary with entries `sum + x` and `sum - x`.

The number of distinct sums is at most `2 × total + 1`, so the work is `O(n × total)`, far smaller than the `2^n` sign choices. (There is also a neat reduction to subset sum: the numbers with `+` have sum `(total + target) / 2`.)

## Explanation

`ways` maps each reachable sum to the number of sign choices that give it. The final answer is the count stored for `target`.
