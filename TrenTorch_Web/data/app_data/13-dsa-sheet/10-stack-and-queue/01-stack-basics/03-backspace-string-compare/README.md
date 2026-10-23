---
name: sheet-backspace-string-compare
title: 'Backspace String Compare'
tags: [dsa-sheet, stack-and-queue, stack-basics]
difficulty: Beginner
---

## Statement

`s` and `t` are typed into empty text editors. A `#` means **backspace** (it deletes the character before it; if the text is empty it does nothing). Return `True` if the two texts are **equal** after all the typing.

For `s = "ab#c"` and `t = "ad#c"` both become `"ac"`.

### Examples

**Example 1**

Input:

```python
backspace_compare('ab#c', 'ad#c')
```

Output:

```text
True
```

**Example 2**

Input:

```python
backspace_compare('a#c', 'b')
```

Output:

```text
False
```

### Constraints

- `0 <= len(s), len(t) <= 200000`
- Letters `a` to `z` and `#`.

## Theory

A text editor is a stack: a letter is pushed and a backspace pops (unless the stack is empty). Build the final text of each string with this rule and compare them.

There is a trick with `O(1)` memory: scan both strings **from the end**, skipping characters that a backspace erases, and compare what is left, but the stack version is the clear first step.

## Explanation

The helper `typed` applies the keys to a list and returns the text; `#` pops only when the list is not empty.
