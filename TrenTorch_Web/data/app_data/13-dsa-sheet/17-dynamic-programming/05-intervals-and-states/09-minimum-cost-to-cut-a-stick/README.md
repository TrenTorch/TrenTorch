---
name: sheet-minimum-cost-to-cut-a-stick
title: 'Minimum Cost to Cut a Stick'
tags: [dsa-sheet, dynamic-programming, intervals-and-states]
difficulty: Mastery
---

## Statement

A stick of length `length` must be cut at the positions in `cuts`, in any order you choose. The cost of one cut is the **current length of the piece being cut**. Return the **smallest total cost**.

For `length = 7` and `cuts = [1, 3, 4, 5]` the answer is `16` (cut at 3, then 5, then 1, then 4: costs 7 + 4 + 3 + 2).

The starter code tries every order of the cuts. It is correct but too slow for many cuts.

### Examples

**Example 1**

Input:

```python
min_cost_cut(7, [1, 3, 4, 5])
```

Output:

```text
16
```

**Example 2**

Input:

```python
min_cost_cut(9, [5, 6, 1, 4, 2])
```

Output:

```text
22
```

### Constraints

- `2 <= length <= 1000000`
- `0 <= len(cuts) <= 100`
- `1 <= cut < length`, all different

## Theory

**Dynamic programming (DP)** solves a problem by combining the answers to smaller versions of the same problem and **remembering** them, so each smaller version is solved only once. It works when the plain recursion keeps asking the same questions (**overlapping subproblems**) and the best answer is built from best answers of smaller parts (**optimal substructure**). The recipe: pick the **state** (what identifies one subproblem), write the **transition** (how a state's answer comes from smaller states), set the **base cases**, and choose the **order**: top-down recursion with a cache, or a bottom-up table. A table often needs only its last row or last few values, which saves memory.

Like burst balloons, think of the **first cut** of a piece. Sort the cuts and add the ends `0` and `length`. For the piece between positions `i` and `j` (indices in this list), choosing the first cut at `k` costs the piece length `points[j] - points[i]` and splits the problem into two independent pieces `(i, k)` and `(k, j)`.

**State:** `cost(i, j)`. **Transition:** `cost(i, j) = points[j] - points[i] + min over k of cost(i, k) + cost(k, j)`. **Base case:** a piece with no cut inside costs 0. Fill by increasing range. `O(m³)` for `m` cuts.

## Explanation

`points` includes both ends; `dp[i][j]` covers the piece between `points[i]` and `points[j]` and `k` is the first cut made in it.
