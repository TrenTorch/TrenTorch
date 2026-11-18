---
name: sheet-distinct-permutations
title: 'Distinct Permutations'
tags: [dsa-sheet, basics, python-toolbox]
difficulty: Intermediate
theory: combinations-permutations-and-meeting-in-the-middle
---

## Statement

Return every different arrangement (permutation) of the characters of `s`, as strings, in alphabetical (lexicographic) order. If `s` has repeated characters, an arrangement that looks the same must be listed only once.

### Examples

**Example 1**

Input:

```python
distinct_permutations('abc')
```

Output:

```text
['abc', 'acb', 'bac', 'bca', 'cab', 'cba']
```

**Example 2**

Input:

```python
distinct_permutations('aab')
```

Output:

```text
['aab', 'aba', 'baa']
```

### Constraints

- `0 <= len(s) <= 8`
- `s` contains only lower-case letters.

## Explanation

Backtracking over the distinct letters, in sorted order, with a count of how many copies of each letter are still unused. At every step try each letter that still has copies left: use one, recurse, put it back. Because each position takes a letter once per distinct letter (not once per copy), no duplicate arrangement is ever built, and sorted letters give sorted output without a final sort.

An empty `s` has exactly one arrangement, the empty string.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                          | Variables                                                              |
| ---------------------------------------- | ---------------------------------------------------------------------- |
| `letters = sorted(Counter(s).items())`   | `letters = [('a', 1), ('b', 1), ('c', 1)]`                             |
| `left = [count for _, count in letters]` | `left = [1, 1, 1]`                                                     |
| `n = len(s)`                             | `n = 3`                                                                |
| `out = []`                               | `out = []`                                                             |
| `prefix = []`                            | `prefix = []`                                                          |
| `def build():`                           | `build = <function distinct_permutations.<locals>.build at 0x00000...` |
| `build()`                                | `out = ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']`                     |
| `return`                                 | `returned = ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']`                |

### Complexity

- Time: O(n * P). `P` is the number of distinct permutations; each one has to be written out (`n` characters), and the backtracking never builds a duplicate.
- Space: O(n). Recursion depth and the current prefix, apart from the output.
