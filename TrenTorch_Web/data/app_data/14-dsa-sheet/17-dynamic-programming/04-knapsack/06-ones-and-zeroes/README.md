---
name: sheet-ones-and-zeroes
title: 'Ones and Zeroes'
tags: [dsa-sheet, dynamic-programming, knapsack]
difficulty: Advanced
theory: counting-versions-and-two-budgets
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

## Explanation

`zeros = s.count("0")` and `ones = len(s) - zeros` are the weights. Both loops run downwards.

### Complexity

- Time: O(len * m * n). Each string updates every `(zeros, ones)` budget once.
- Space: O(m * n). The table of budgets.
