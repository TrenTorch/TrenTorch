---
name: sheet-decode-string
title: 'Decode a String'
tags: [dsa-sheet, stack-and-queue, stack-basics]
difficulty: Intermediate
---

## Statement

The encoding rule is `k[text]`: the `text` inside the square brackets is repeated exactly `k` times. Brackets can be **nested**. Return the decoded string.

For `"3[a2[c]]"` the answer is `"accaccacc"`; for `"2[ab]3[c]"` it is `"ababccc"`.

### Examples

**Example 1**

Input:

```python
decode_string('3[a2[c]]')
```

Output:

```text
'accaccacc'
```

**Explanation:** The inner 2[c] becomes cc, making the expression 3[acc], which resolves to accaccacc.

**Example 2**

Input:

```python
decode_string('2[ab]3[c]')
```

Output:

```text
'ababccc'
```

**Explanation:** The string 2[ab] becomes abab and 3[c] becomes ccc, which concatenate to produce ababccc.

### Constraints

- `0 <= len(s) <= 2000`
- `s` has lower-case letters, digits and brackets, and is always valid.
- `k` is a number from 1 to 300 and the decoded length is at most 200000.

## Theory

A **stack** is last in, first out: you only add (`push`) and remove (`pop`) at the top. In Python a list does this with `append()` and `pop()`, both `O(1)`.

Nested structure is the signal for a stack. Read the characters left to right and keep the **current text** and the **current number**. When you meet `[`, you are going one level deeper: **push** the text built so far and the repeat count onto the stack, then start a fresh empty text. When you meet `]`, the level ends: **pop** the saved text and count, and set `current = saved_text + current * count`.

Digits can have several characters (`"12[a]"`), so build the number digit by digit. The recursion alternative is the same idea with the call stack as the stack.

## Explanation

`num` collects the digits before `[`. At `[`, `(text, num)` is saved and both reset. At `]`, the text built inside the brackets is repeated and glued to the saved text.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line               | Variables                                                           |
| ----------------------------- | ------------------------------------------------------------------- |
| `stack = []`                  | `stack = []`                                                        |
| `for ch in s:`                | `text = '', num = 0, ch = '3'`                                      |
| `stack.append((text, num))`   | `stack = [('', 3)], num = 3, ch = '['`                              |
| `text += ch`                  | `text = 'a', num = 0, ch = 'a'`                                     |
| `stack.append((text, num))`   | `stack = [('', 3), ('a', 2)], num = 2, ch = '['`                    |
| `text += ch`                  | `text = 'c', num = 0, ch = 'c'`                                     |
| `text = saved + text * count` | `stack = [('', 3)], text = 'acc', ch = ']', saved = 'a', count = 2` |
| `return`                      | `returned = 'accaccacc'`                                            |
