---
name: sheet-remove-duplicate-letters
title: 'Smallest String With Each Letter Once'
tags: [dsa-sheet, greedy, greedy-strategies]
difficulty: Mastery
theory: smallest-string-with-each-letter-once
---

## Statement

Remove letters from `s` so that **every letter that appears in `s` appears exactly once**, keeping the original relative order. Among all possible results return the one that is **smallest in dictionary order**.

For `"bcabc"` the answer is `"abc"`; for `"cbacdcbc"` it is `"acdb"`.

### Examples

**Example 1**

Input:

```python
remove_duplicate_letters('bcabc')
```

Output:

```text
'abc'
```

**Example 2**

Input:

```python
remove_duplicate_letters('cbacdcbc')
```

Output:

```text
'acdb'
```

### Constraints

- `0 <= len(s) <= 200000`
- Lower-case letters.

## Explanation

A popped letter is not lost: a later copy exists. Letters already on the stack are skipped, since keeping the earlier occurrence is never worse after the pops.

### Complexity

- Time: O(n). Each character is pushed and popped at most once.
- Space: O(k). The stack and set hold at most one entry per letter, `k` <= 26.
