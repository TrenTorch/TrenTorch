---
name: sheet-partition-equal-subset-sum
title: 'Partition Equal Subset Sum'
tags: [dsa-sheet, dynamic-programming, sequences-and-counting]
difficulty: Intermediate
---

## Statement

Return `True` if the numbers in `nums` can be split into **two groups with the same sum**.

For `[1, 5, 11, 5]` the answer is `True` (`11` and `1 + 5 + 5`); for `[1, 2, 3, 5]` it is `False`.

The starter code tries to include or skip every number. It is correct but too slow on inputs without an answer.

### Examples

**Example 1**

Input:

```python
can_partition([1, 5, 11, 5])
```

Output:

```text
True
```

**Example 2**

Input:

```python
can_partition([1, 2, 3, 5])
```

Output:

```text
False
```

### Constraints

- `0 <= len(nums) <= 200`
- `1 <= nums[i] <= 100`

## Theory

**Dynamic programming (DP)** solves a problem by combining the answers to smaller versions of the same problem and **remembering** them, so each smaller version is solved only once. It works when the plain recursion keeps asking the same questions (**overlapping subproblems**) and the best answer is built from best answers of smaller parts (**optimal substructure**). The recipe: pick the **state** (what identifies one subproblem), write the **transition** (how a state's answer comes from smaller states), set the **base cases**, and choose the **order**: top-down recursion with a cache, or a bottom-up table. A table often needs only its last row or last few values, which saves memory.

Two equal groups means one group has sum `total / 2`. If `total` is odd the answer is `False`. Otherwise this is the **subset sum** problem: can some subset of the numbers add up to `half`?

**State:** `reach(s)`, whether some subset sums to exactly `s`. **Transition:** processing one number `x` at a time, `reach(s)` becomes true if `reach(s)` was already true or `reach(s - x)` was true. **Base case:** `reach(0) = True`. Update `s` **downwards** so a number is not used twice.

Python tip: the whole table is one big integer used as a **bitset**: bit `s` is set when sum `s` is reachable, and adding a number `x` is `bits |= bits << x`. That runs in `O(n × half / 64)`.

## Explanation

Bit `s` of `bits` means "a subset with sum `s` exists". The shift by `x` adds `x` to every reachable sum at once.
