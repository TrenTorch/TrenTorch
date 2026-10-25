---
name: sheet-remove-duplicate-letters
title: 'Smallest String With Each Letter Once'
tags: [dsa-sheet, greedy, greedy-strategies]
difficulty: Mastery
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

**Explanation:** Input 'bcabc' has letters a b c. The smallest string with each exactly once is 'abc'.

**Example 2**

Input:

```python
remove_duplicate_letters('cbacdcbc')
```

Output:

```text
'acdb'
```

**Explanation:** Input 'cbacdcbc' contains letters a b c d. The minimal string preserving order with each once is 'acdb'.

### Constraints

- `0 <= len(s) <= 200000`
- Lower-case letters.

## Theory

A **greedy** algorithm builds the answer step by step and, at each step, takes the choice that looks best **right now**, without ever going back. It is fast and simple, but it is only correct when the problem has a structure that makes local choices safe. The hard part is the **proof**: show that the greedy choice can always be part of some best answer.

Build the result with a **stack**, scanning left to right. For each letter `c` (skip it if it is already in the stack): while the **top** of the stack is **bigger** than `c` **and appears again later** in the string, pop it (it can be placed later, and `c` gives a smaller string now). Then push `c`.

You need two helper facts: `last[ch]` (the last position of each letter, to know if it appears again) and a set `in_stack`. The condition "appears again later" is `last[top] > i`.

This is the same idea as removing digits to get the smallest number, with the extra constraint that you cannot drop the last copy of a letter. `O(n)`.

## Explanation

A popped letter is not lost: a later copy exists. Letters already on the stack are skipped, since keeping the earlier occurrence is never worse after the pops.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                            | Variables                                                    |
| ------------------------------------------ | ------------------------------------------------------------ |
| `last = {ch: i for i, ch in enumerate(s)}` | `last = {'b': 3, 'c': 4, 'a': 2}`                            |
| `for i, ch in enumerate(s):`               | `stack = [], in_stack = set(), i = 0, ch = 'b'`              |
| `for i, ch in enumerate(s):`               | `stack = ['b'], in_stack = {'b'}, i = 1, ch = 'c'`           |
| `for i, ch in enumerate(s):`               | `stack = ['b', 'c'], in_stack = {'c', 'b'}, i = 2, ch = 'a'` |
| `in_stack.discard(stack.pop())`            | `stack = [], in_stack = set()`                               |
| `for i, ch in enumerate(s):`               | `stack = ['a'], in_stack = {'a'}, i = 3, ch = 'b'`           |
| `for i, ch in enumerate(s):`               | `stack = ['a', 'b'], in_stack = {'a', 'b'}, i = 4, ch = 'c'` |
| `return`                                   | `returned = 'abc'`                                           |
