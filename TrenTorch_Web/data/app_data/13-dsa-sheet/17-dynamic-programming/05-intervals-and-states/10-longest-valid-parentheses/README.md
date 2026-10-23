---
name: sheet-longest-valid-parentheses
title: 'Longest Valid Parentheses'
tags: [dsa-sheet, dynamic-programming, intervals-and-states]
difficulty: Advanced
---

## Statement

`s` contains only `(` and `)`. Return the length of the **longest substring** (consecutive characters) that is a **valid** parentheses string (every `(` closed in the right order).

For `")()())"` the answer is `4`.

The starter code checks every substring. It is correct but too slow for long strings.

### Examples

**Example 1**

Input:

```python
longest_valid_parentheses(')()())')
```

Output:

```text
4
```

**Example 2**

Input:

```python
longest_valid_parentheses('(()')
```

Output:

```text
2
```

### Constraints

- `0 <= len(s) <= 200000`

## Theory

**Dynamic programming (DP)** solves a problem by combining the answers to smaller versions of the same problem and **remembering** them, so each smaller version is solved only once. It works when the plain recursion keeps asking the same questions (**overlapping subproblems**) and the best answer is built from best answers of smaller parts (**optimal substructure**). The recipe: pick the **state** (what identifies one subproblem), write the **transition** (how a state's answer comes from smaller states), set the **base cases**, and choose the **order**: top-down recursion with a cache, or a bottom-up table. A table often needs only its last row or last few values, which saves memory.

**State:** `valid[i]`, the length of the longest valid substring **ending exactly at `i`**. **Transition:** only a `)` can end a valid block.

- If `s[i - 1] == '('`: the pair `()` closes: `valid[i] = valid[i - 2] + 2`.
- Else (`s[i - 1] == ')'`) look before the valid block ending at `i - 1`: the character at `j = i - valid[i - 1] - 1`; if it is `(` it matches this `)`: `valid[i] = valid[i - 1] + 2 + valid[j - 1]`.

The answer is the maximum. `O(n)`. A **stack of indices** solves it as well: keep the index of the last unmatched position as a base, and the answer at each `)` is `i - stack[-1]` after popping.

## Explanation

The stack holds the indices of unmatched characters; its top is the start boundary. A `)` pops a match and measures the length from the new top.
