---
name: sheet-valid-palindrome-ii
title: 'Palindrome After Deleting One Character'
tags: [dsa-sheet, two-pointers, two-pointers]
difficulty: Intermediate
---

## Statement

Return `True` if `s` can become a **palindrome** (reads the same both ways) by deleting **at most one** character. `"abca"` works (delete `c` or `b`); `"abc"` does not.

### Examples

**Example 1**

Input:

```python
valid_palindrome_ii('aba')
```

Output:

```text
True
```

**Example 2**

Input:

```python
valid_palindrome_ii('abca')
```

Output:

```text
True
```

### Constraints

- `0 <= len(s) <= 200000`
- Lower-case letters.

## Theory

**Two pointers** means keeping two positions in the data (often one at each end, or one behind the other) and moving them according to a rule, so that each position moves at most `n` times in total. That turns a double loop (`O(n²)`) into a single pass (`O(n)`).

Check a palindrome with a pointer at each end, moving inwards while the characters match. The first time they **differ**, you have used up your one deletion: either the left or the right character must go. Try both: is `s[left + 1 .. right]` a palindrome, or is `s[left .. right - 1]`? Each is an ordinary two-pointer check.

Only one mismatch needs this branching, so the whole thing is still `O(n)`.

## Explanation

`is_pal(i, j)` is the plain check. At the first mismatch, one of the two characters is dropped and the rest must match completely.
