---
name: sheet-letter-combinations
title: 'Phone Keypad Letters'
tags: [dsa-sheet, recursion, backtracking-puzzles]
difficulty: Beginner
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

## Theory

At each digit you **choose one of its letters**, then move on to the next digit: a recursion of depth `len(digits)`, branching 3 or 4 ways each time. The base case is when every digit has been used: record the string built so far.

Because the letters of a key are in alphabetical order and you handle the digits left to right, the results come out in dictionary order without sorting.

You can also do it iteratively: start with `[""]` and for each digit replace every string `s` by `s + letter` for each letter. That is the same idea written as a loop (`itertools.product` does it too).

## Explanation

`go(i, prefix)` appends each letter of digit `i` to the prefix and recurses to the next digit; at `i == len(digits)` the prefix is a full answer. An empty digit string returns `[]`, not `[""]`.
