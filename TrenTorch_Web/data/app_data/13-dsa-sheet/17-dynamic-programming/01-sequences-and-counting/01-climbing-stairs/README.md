---
name: sheet-climbing-stairs
title: 'Climbing Stairs'
tags: [dsa-sheet, dynamic-programming, sequences-and-counting]
difficulty: Beginner
---

## Statement

You climb a staircase with `n` steps. Each move goes up **1 or 2** steps. Return the **number of different ways** to reach the top, modulo `10**9 + 7`.

For `n = 3` the answer is `3` (`1+1+1`, `1+2`, `2+1`).

The starter code is a plain recursion. It is correct but far too slow for large `n`.

### Examples

**Example 1**

Input:

```python
climb_stairs(3)
```

Output:

```text
3
```

**Example 2**

Input:

```python
climb_stairs(5)
```

Output:

```text
8
```

### Constraints

- `0 <= n <= 1000000`

## Theory

**Dynamic programming (DP)** solves a problem by combining the answers to smaller versions of the same problem and **remembering** them, so each smaller version is solved only once. It works when the plain recursion keeps asking the same questions (**overlapping subproblems**) and the best answer is built from best answers of smaller parts (**optimal substructure**). The recipe: pick the **state** (what identifies one subproblem), write the **transition** (how a state's answer comes from smaller states), set the **base cases**, and choose the **order**: top-down recursion with a cache, or a bottom-up table. A table often needs only its last row or last few values, which saves memory.

**State:** `ways(i)`, the number of ways to reach step `i`. **Transition:** the last move came from step `i - 1` or step `i - 2`, so `ways(i) = ways(i - 1) + ways(i - 2)`. **Base cases:** `ways(0) = ways(1) = 1`. These are the **Fibonacci numbers**.

The recursion `ways(n - 1) + ways(n - 2)` computes `ways(n - 3)` twice, `ways(n - 4)` three times, and so on: the number of calls grows exponentially. Computing the values **in order** from the bottom and keeping only the last two removes all the repetition: `O(n)` time and `O(1)` memory.

## Explanation

`a` and `b` are the last two values. Each loop round shifts them forward by one step, taking the sum modulo `10**9 + 7` to keep the numbers small.
