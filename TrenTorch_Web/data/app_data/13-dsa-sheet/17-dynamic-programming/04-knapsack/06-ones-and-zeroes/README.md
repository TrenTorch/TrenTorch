---
name: sheet-ones-and-zeroes
title: 'Ones and Zeroes'
tags: [dsa-sheet, dynamic-programming, knapsack]
difficulty: Advanced
---

## Statement

`strs` is a list of binary strings. Return the **largest number of strings** you can pick so that together they contain **at most `m` zeros and at most `n` ones**. Each string can be picked once.

For `strs = ["10", "0001", "111001", "1", "0"]`, `m = 5` and `n = 3` the answer is `4`.

### Examples

**Example 1**

Input:

```python
find_max_form(['10', '0001', '111001', '1', '0'], 5, 3)
```

Output:

```text
4
```

**Example 2**

Input:

```python
find_max_form(['10', '0', '1'], 1, 1)
```

Output:

```text
2
```

### Constraints

- `0 <= len(strs) <= 200`
- `1 <= len(string) <= 20`
- `0 <= m, n <= 60`

## Theory

**Dynamic programming (DP)** solves a problem by combining the answers to smaller versions of the same problem and **remembering** them, so each smaller version is solved only once. It works when the plain recursion keeps asking the same questions (**overlapping subproblems**) and the best answer is built from best answers of smaller parts (**optimal substructure**). The recipe: pick the **state** (what identifies one subproblem), write the **transition** (how a state's answer comes from smaller states), set the **base cases**, and choose the **order**: top-down recursion with a cache, or a bottom-up table. A table often needs only its last row or last few values, which saves memory.

This is a 0/1 knapsack with **two capacities** (zeros and ones) and every item worth 1. **State:** `best[z][o]`, the most strings you can take using at most `z` zeros and `o` ones. **Transition:** for a string with `a` zeros and `b` ones, `best[z][o] = max(best[z][o], 1 + best[z - a][o - b])` for `z >= a, o >= b`. Loop `z` and `o` **downwards** so each string is used once. `O(len(strs) × m × n)`.

## Explanation

`zeros = s.count("0")` and `ones = len(s) - zeros` are the weights. Both loops run downwards.
