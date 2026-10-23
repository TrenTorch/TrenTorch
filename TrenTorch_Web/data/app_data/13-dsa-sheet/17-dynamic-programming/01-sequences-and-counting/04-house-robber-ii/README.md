---
name: sheet-house-robber-ii
title: 'House Robber on a Circle'
tags: [dsa-sheet, dynamic-programming, sequences-and-counting]
difficulty: Intermediate
---

## Statement

The houses now stand in a **circle**: the last house is a neighbour of the first. You still cannot rob two neighbouring houses. Return the **largest total** you can take.

For `[2, 3, 2]` the answer is `3` (houses 0 and 2 are neighbours).

### Examples

**Example 1**

Input:

```python
rob_circle([2, 3, 2])
```

Output:

```text
3
```

**Example 2**

Input:

```python
rob_circle([1, 2, 3, 1])
```

Output:

```text
4
```

### Constraints

- `0 <= len(nums) <= 300000`
- `0 <= nums[i] <= 10000`

## Theory

**Dynamic programming (DP)** solves a problem by combining the answers to smaller versions of the same problem and **remembering** them, so each smaller version is solved only once. It works when the plain recursion keeps asking the same questions (**overlapping subproblems**) and the best answer is built from best answers of smaller parts (**optimal substructure**). The recipe: pick the **state** (what identifies one subproblem), write the **transition** (how a state's answer comes from smaller states), set the **base cases**, and choose the **order**: top-down recursion with a cache, or a bottom-up table. A table often needs only its last row or last few values, which saves memory.

The new rule only adds one constraint: the first and the last house cannot both be robbed. So split into two **line** problems and take the better:

- the first house is **not** robbed: solve the line `nums[1:]`;
- the last house is **not** robbed: solve the line `nums[:-1]`.

One of the two cases covers the optimal choice, because at most one of the two ends is robbed. Solve each line with the house robber recurrence. A single house is a special case: its own value. `O(n)`.

## Explanation

`line` is the previous question's loop. The answer is the larger of the two lines that each drop one end.
