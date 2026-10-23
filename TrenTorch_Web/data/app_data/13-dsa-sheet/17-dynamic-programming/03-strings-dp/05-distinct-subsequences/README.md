---
name: sheet-distinct-subsequences
title: 'Distinct Subsequences'
tags: [dsa-sheet, dynamic-programming, strings-dp]
difficulty: Advanced
---

## Statement

Return the **number of ways** to pick characters of `s` (keeping their order) that spell `t`. Different choices of positions count as different ways. Return the answer modulo `10**9 + 7`.

For `s = "rabbbit"` and `t = "rabbit"` the answer is `3`.

The starter code is a plain recursion. It is correct but too slow for long strings.

### Examples

**Example 1**

Input:

```python
num_distinct('rabbbit', 'rabbit')
```

Output:

```text
3
```

**Example 2**

Input:

```python
num_distinct('babgbag', 'bag')
```

Output:

```text
5
```

### Constraints

- `0 <= len(s) <= 2000`
- `0 <= len(t) <= 500`
- Lower-case letters.

## Theory

**Dynamic programming (DP)** solves a problem by combining the answers to smaller versions of the same problem and **remembering** them, so each smaller version is solved only once. It works when the plain recursion keeps asking the same questions (**overlapping subproblems**) and the best answer is built from best answers of smaller parts (**optimal substructure**). The recipe: pick the **state** (what identifies one subproblem), write the **transition** (how a state's answer comes from smaller states), set the **base cases**, and choose the **order**: top-down recursion with a cache, or a bottom-up table. A table often needs only its last row or last few values, which saves memory.

**State:** `ways(i, j)`, the number of ways to spell the first `j` characters of `t` using the first `i` characters of `s`. **Transition:** the character `s[i - 1]` is either skipped, which keeps `ways(i - 1, j)`, or used as the last letter of `t[:j]` when they match, which adds `ways(i - 1, j - 1)`: `ways(i, j) = ways(i - 1, j) + (ways(i - 1, j - 1) if s[i-1] == t[j-1])`. **Base cases:** `ways(i, 0) = 1` (spell the empty string by choosing nothing).

One row suffices if `j` runs **downwards**, so that `ways[j - 1]` still holds the old row. `O(len(s) × len(t))`.

## Explanation

`row[j]` is the number of ways to spell `t[:j]` with the characters seen so far. Iterating `j` downwards uses the previous row's `row[j - 1]`.
