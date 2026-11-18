---
name: sheet-generate-parentheses
title: 'Generate Parentheses'
tags: [dsa-sheet, recursion, backtracking-puzzles]
difficulty: Intermediate
theory: balanced-brackets
---

## Statement

Return every **valid** string made of `n` pairs of parentheses (every `(` has a matching `)` after it), listed in dictionary order (`(` comes before `)`). For `n = 3`: `((())), (()()), (())(), ()(()), ()()()`.

### Examples

**Example 1**

Input:

```python
generate_parentheses(3)
```

Output:

```text
['((()))', '(()())', '(())()', '()(())', '()()()']
```

**Example 2**

Input:

```python
generate_parentheses(1)
```

Output:

```text
['()']
```

### Constraints

- `0 <= n <= 10`

## Explanation

`go(prefix, opens, closes)` adds `(` while `opens < n` and `)` while `closes < opens`. When the prefix has `2n` characters it is complete and valid. Because `(` is tried first the strings come out sorted.

### Complexity

- Time: O(n * C(n)). `C(n)`, the n-th Catalan number (about `4^n / n^1.5`), strings of length `2n`; the two prune rules never build an invalid prefix.
- Space: O(n * C(n)). The output; the recursion adds only `O(n^2)` for the prefixes on the current path.
