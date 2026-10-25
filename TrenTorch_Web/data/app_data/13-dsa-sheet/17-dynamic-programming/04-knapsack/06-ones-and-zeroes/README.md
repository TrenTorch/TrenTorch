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

**Explanation:** Pick "10", "0001", "1", "0" giving exactly five zeros and three ones, total four strings.

**Example 2**

Input:

```python
find_max_form(['10', '0', '1'], 1, 1)
```

Output:

```text
2
```

**Explanation:** Pick "0" and "1" using one zero and one one, yielding two strings.

### Constraints

- `0 <= len(strs) <= 200`
- `1 <= len(string) <= 20`
- `0 <= m, n <= 60`

## Theory

**Dynamic programming (DP)** solves a problem by combining the answers to smaller versions of the same problem and **remembering** them, so each smaller version is solved only once. It works when the plain recursion keeps asking the same questions (**overlapping subproblems**) and the best answer is built from best answers of smaller parts (**optimal substructure**). The recipe: pick the **state** (what identifies one subproblem), write the **transition** (how a state's answer comes from smaller states), set the **base cases**, and choose the **order**: top-down recursion with a cache, or a bottom-up table. A table often needs only its last row or last few values, which saves memory.

This is a 0/1 knapsack with **two capacities** (zeros and ones) and every item worth 1. **State:** `best[z][o]`, the most strings you can take using at most `z` zeros and `o` ones. **Transition:** for a string with `a` zeros and `b` ones, `best[z][o] = max(best[z][o], 1 + best[z - a][o - b])` for `z >= a, o >= b`. Loop `z` and `o` **downwards** so each string is used once. `O(len(strs) × m × n)`.

## Explanation

`zeros = s.count("0")` and `ones = len(s) - zeros` are the weights. Both loops run downwards.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                                | Variables                                                                                                                                                     |
| ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `best = [[0] * (n + 1) for _ in range(m + 1)]` | `best = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], ...`                                                                                         |
| `row[o] = source[o - ones] + 1`                | `best = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 1, 1], ..., s = '10', zeros = 1, ones = 1, z = 3, row = [0, 0, 1, 1], source = [0, 0, 0, 0], o = 2` |
| `row[o] = source[o - ones] + 1`                | `best = [[0, 0, 0, 0], [0, 1, 1, 1], [0, 1, 1, 1], [0, 1, 1, 1], ..., s = '0001', zeros = 3, z = 5, row = [0, 1, 2, 2], source = [0, 1, 1, 1]`                |
| `for s in strs:`                               | `s = '1', zeros = 2, ones = 4, z = 2, row = [0, 1, 1, 1], source = [0, 0, 0, 0], o = 1`                                                                       |
| `for z in range(m, zeros - 1, -1):`            | `best = [[0, 0, 0, 0], [0, 1, 1, 1], [0, 1, 1, 1], [0, 1, 2, 2], ..., zeros = 0, ones = 1, row = [0, 1, 2, 2], source = [0, 1, 2, 2]`                         |
| `zeros = s.count("0")`                         | `best = [[0, 1, 1, 1], [0, 1, 2, 2], [0, 1, 2, 2], [0, 1, 2, 2], ..., s = '0', zeros = 1, z = 0, row = [0, 1, 1, 1], source = [0, 1, 1, 1]`                   |
| `row[o] = source[o - ones] + 1`                | `best = [[0, 1, 1, 1], [0, 1, 2, 2], [0, 1, 2, 2], [0, 1, 2, 3], ..., ones = 0, z = 3, row = [0, 1, 2, 3], source = [0, 1, 2, 2], o = 3`                      |
| `return`                                       | `returned = 4`                                                                                                                                                |
