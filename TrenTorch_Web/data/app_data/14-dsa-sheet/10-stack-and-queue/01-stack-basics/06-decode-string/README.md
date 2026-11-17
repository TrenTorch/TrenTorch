---
name: sheet-decode-string
title: 'Decode a String'
tags: [dsa-sheet, stack-and-queue, stack-basics]
difficulty: Intermediate
theory: nested-repeats
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

**Example 2**

Input:

```python
decode_string('2[ab]3[c]')
```

Output:

```text
'ababccc'
```

### Constraints

- `0 <= len(s) <= 2000`
- `s` has lower-case letters, digits and brackets, and is always valid.
- `k` is a number from 1 to 300 and the decoded length is at most 200000.

## Explanation

Write everything into one list of characters. When a `[` opens, remember where the output is now and the repeat count. When the matching `]` closes, the characters written since then are the block: repeat them `count - 1` more times at the end (nothing to do for `1`, and drop the block for `0`).

Because a block is only copied when it is repeated, the work stays proportional to the length of the output instead of copying the same text again for every nesting level.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                         | Variables                                                                       |
| --------------------------------------- | ------------------------------------------------------------------------------- |
| `out = []`                              | `out = []`                                                                      |
| `for ch in s:`                          | `open_blocks = [], num = 0, ch = '3'`                                           |
| `open_blocks.append((len(out), num))`   | `open_blocks = [(0, 3)], num = 3, ch = '['`                                     |
| `out.append(ch)`                        | `out = ['a'], num = 0, ch = 'a'`                                                |
| `open_blocks.append((len(out), num))`   | `open_blocks = [(0, 3), (1, 2)], num = 2, ch = '['`                             |
| `out.append(ch)`                        | `out = ['a', 'c'], num = 0, ch = 'c'`                                           |
| `out.extend(out[start:] * (count - 1))` | `out = ['a', 'c', 'c'], open_blocks = [(0, 3)], ch = ']', start = 1, count = 2` |
| `return`                                | `returned = 'accaccacc'`                                                        |

### Complexity

- Time: O(n + L). One pass over the input, writing into a single buffer; a repeat copies only the part it repeats, so the work matches the length `L` of the output.
- Space: O(n + L). The output buffer and the stack of open brackets.
