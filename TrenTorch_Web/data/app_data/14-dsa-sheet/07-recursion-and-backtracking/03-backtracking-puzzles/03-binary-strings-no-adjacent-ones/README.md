---
name: sheet-binary-strings-no-adjacent-ones
title: 'Binary Strings Without Two Ones in a Row'
tags: [dsa-sheet, recursion, backtracking-puzzles]
difficulty: Beginner
theory: a-rule-on-the-next-choice
---

## Statement

Return every **binary string of length `n`** (made of `0` and `1`) that does **not** contain two `1`s next to each other, in dictionary order. For `n = 3`: `000, 001, 010, 100, 101`. For `n = 0` the answer is the single empty string `[""]`.

### Examples

**Example 1**

Input:

```python
no_adjacent_ones(3)
```

Output:

```text
['000', '001', '010', '100', '101']
```

**Example 2**

Input:

```python
no_adjacent_ones(0)
```

Output:

```text
['']
```

### Constraints

- `0 <= n <= 16`
- The answer has about `1.6^n` strings (4,181 for `n = 18`).

## Explanation

`go(prefix)` returns when the prefix has length `n`. It always tries adding `0`, and tries adding `1` only when the prefix is empty or does not end in `1`.

### Complexity

- Time: O(n * F(n)). The number of valid strings is a Fibonacci number, about `1.618^n`, and the check "no `1` after `1`" prunes the rest.
- Space: O(n * F(n)). The output.
