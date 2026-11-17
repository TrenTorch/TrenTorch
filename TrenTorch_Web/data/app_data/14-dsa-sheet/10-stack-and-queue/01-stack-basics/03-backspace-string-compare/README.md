---
name: sheet-backspace-string-compare
title: 'Backspace String Compare'
tags: [dsa-sheet, stack-and-queue, stack-basics]
difficulty: Beginner
theory: typing-with-a-backspace-key
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

## Explanation

Compare the two strings from the right, so that a `#` is seen before the characters it erases. A helper moves an index left to the next character that is really typed, counting `#` marks as characters to skip. If the two helpers land on different characters, or only one string has a character left, the results differ. Reaching the start of both at the same time means they are equal. No stack or copy is needed.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                 | Variables                                                                   |
| ------------------------------- | --------------------------------------------------------------------------- |
| `def next_typed(text, i):`      | `next_typed = <function backspace_compare.<locals>.next_typed at 0x0000...` |
| `i, j = len(s) - 1, len(t) - 1` | `i = 3, j = 3`                                                              |
| `i -= 1`                        | `i = 2`                                                                     |
| `j -= 1`                        | `j = 2`                                                                     |
| `j = next_typed(t, j)`          | `i = 0, j = 0`                                                              |
| `i -= 1`                        | `i = -1`                                                                    |
| `j -= 1`                        | `j = -1`                                                                    |
| `return`                        | `returned = True`                                                           |

### Complexity

- Time: O(n + m). Both strings are scanned once from the right; a counter skips the characters a backspace erases.
- Space: O(1). A few indices and counters.
