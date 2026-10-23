---
name: sheet-subset-sum
title: 'Subset Sum'
tags: [dsa-sheet, dynamic-programming, knapsack]
difficulty: Intermediate
---

## Statement

Return `True` if some **subset** of `nums` (possibly empty) adds up to exactly `target`.

For `nums = [3, 34, 4, 12, 5, 2]` and `target = 9` the answer is `True` (`4 + 5`).

The starter code tries taking or skipping every number. It is correct but too slow when there is no answer.

### Examples

**Example 1**

Input:

```python
subset_sum([3, 34, 4, 12, 5, 2], 9)
```

Output:

```text
True
```

**Example 2**

Input:

```python
subset_sum([3, 34, 4, 12, 5, 2], 30)
```

Output:

```text
False
```

### Constraints

- `0 <= len(nums) <= 200`
- `1 <= nums[i] <= 1000`
- `0 <= target <= 100000`

## Theory

**Dynamic programming (DP)** solves a problem by combining the answers to smaller versions of the same problem and **remembering** them, so each smaller version is solved only once. It works when the plain recursion keeps asking the same questions (**overlapping subproblems**) and the best answer is built from best answers of smaller parts (**optimal substructure**). The recipe: pick the **state** (what identifies one subproblem), write the **transition** (how a state's answer comes from smaller states), set the **base cases**, and choose the **order**: top-down recursion with a cache, or a bottom-up table. A table often needs only its last row or last few values, which saves memory.

**State:** `reach(s)`, whether some subset sums to exactly `s`. **Transition:** after considering a number `x`, `reach(s)` is true if it was true before, or `reach(s - x)` was true. **Base case:** `reach(0) = True`.

In Python the whole table fits in **one integer used as a bitset**: bit `s` is set when `s` is reachable, and adding the number `x` is `bits |= bits << x`. Mask off bits above `target` to keep the integer small. `O(n × target / 64)` machine operations.

## Explanation

The shift by `x` adds `x` to every reachable sum at once, and the mask drops sums larger than the target.
