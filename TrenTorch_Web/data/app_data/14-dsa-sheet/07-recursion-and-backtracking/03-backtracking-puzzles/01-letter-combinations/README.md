---
name: sheet-letter-combinations
title: 'Phone Keypad Letters'
tags: [dsa-sheet, recursion, backtracking-puzzles]
difficulty: Beginner
theory: a-menu-for-every-position
---

## Statement

On a phone keypad each digit from `2` to `9` stands for letters: `2: abc`, `3: def`, `4: ghi`, `5: jkl`, `6: mno`, `7: pqrs`, `8: tuv`, `9: wxyz`. Given a string of such digits, return **every string** the digits could spell, in dictionary order. An empty string of digits gives an empty list.

For `"23"`: `ad, ae, af, bd, be, bf, cd, ce, cf`.

### Examples

**Example 1**

Input:

```python
letter_combinations('23')
```

Output:

```text
['ad', 'ae', 'af', 'bd', 'be', 'bf', 'cd', 'ce', 'cf']
```

**Example 2**

Input:

```python
letter_combinations('')
```

Output:

```text
[]
```

### Constraints

- `0 <= len(digits) <= 8`
- Every character is a digit from `2` to `9`.

## Explanation

`go(i, prefix)` appends each letter of digit `i` to the prefix and recurses to the next digit; at `i == len(digits)` the prefix is a full answer. An empty digit string returns `[]`, not `[""]`.

### Complexity

- Time: O(n * 4^n). There are at most `4^n` combinations of `n` digits, each of length `n`.
- Space: O(n * 4^n). The output.
