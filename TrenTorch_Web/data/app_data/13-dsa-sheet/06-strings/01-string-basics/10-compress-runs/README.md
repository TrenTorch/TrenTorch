---
name: sheet-compress-runs
title: 'Compress Repeated Characters'
tags: [dsa-sheet, strings, string-basics]
difficulty: Beginner
---

## Statement

Compress `s` by replacing every **run** of the same character with that character followed by the length of the run. A run of length `1` is written as just the character (no `1`).

For example `"aabcccccaaa"` becomes `"a2bc5a3"`.

### Examples

**Example 1**

Input:

```python
compress_runs('aabcccccaaa')
```

Output:

```text
'a2bc5a3'
```

**Explanation:** The input has runs: 'aa' (2), 'b' (1), 'ccccc' (5), 'aaa' (3); each run becomes the character plus its length if greater than one, yielding 'a2bc5a3'.

**Example 2**

Input:

```python
compress_runs('abc')
```

Output:

```text
'abc'
```

**Explanation:** All characters appear singly, so each run length is one and no numbers are appended, leaving the string unchanged.

### Constraints

- `0 <= len(s) <= 3 * 10**5`
- `s` contains lower-case letters.

## Theory

This is **run-length encoding**. Scan the string and keep the current character and how many times it has repeated. When the next character differs (or the string ends), write out the finished run and start a new one.

`itertools.groupby(s)` does the grouping for you: it yields `(character, run)` pairs for consecutive equal characters, so a run's length is `sum(1 for _ in run)`. Collect the pieces in a list and `join` them once, because `+=` on a long string in a loop is slow.

## Explanation

`groupby(s)` splits `s` into runs of equal characters. For each run write the character, plus its length when it is more than one. The pieces are joined once at the end.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                                | Variables                                                                           |
| ---------------------------------------------- | ----------------------------------------------------------------------------------- |
| `parts = []`                                   | `parts = []`                                                                        |
| `n = sum(1 for _ in run)`                      | `ch = 'a', run = <itertools._grouper object at 0x000001F4854830A0>, n = 2`          |
| `for ch, run in groupby(s):`                   | `parts = ['a2'], ch = 'b', run = <itertools._grouper object at 0x000001F485481960>` |
| `parts.append(ch + (str(n) if n > 1 else ""))` | `parts = ['a2', 'b'], n = 1`                                                        |
| `for ch, run in groupby(s):`                   | `ch = 'c', run = <itertools._grouper object at 0x000001F4854830A0>`                 |
| `parts.append(ch + (str(n) if n > 1 else ""))` | `parts = ['a2', 'b', 'c5'], n = 5`                                                  |
| `n = sum(1 for _ in run)`                      | `ch = 'a', run = <itertools._grouper object at 0x000001F485481960>, n = 3`          |
| `return`                                       | `returned = 'a2bc5a3'`                                                              |

### Complexity

- Time: O(n) where n is length of s.
- Extra space: O(n) for output string and parts list.
- The brute force takes O(n) where n is length of s.
