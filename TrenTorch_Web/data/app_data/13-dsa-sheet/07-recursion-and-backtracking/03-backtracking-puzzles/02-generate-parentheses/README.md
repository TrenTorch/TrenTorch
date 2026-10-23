---
name: sheet-generate-parentheses
title: 'Generate Parentheses'
tags: [dsa-sheet, recursion, backtracking-puzzles]
difficulty: Intermediate
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

## Theory

Building all `2^(2n)` strings of `(` and `)` and filtering the valid ones wastes almost everything. Instead **only build valid prefixes**. At each position you may add:

- a `(` if you have used fewer than `n` of them, and
- a `)` only if it would still be matched: the number of `)` used so far must be smaller than the number of `(`.

A prefix that follows these two rules can always be finished into a valid string, so every branch of the recursion leads to an answer. Trying `(` before `)` gives dictionary order.

The number of valid strings is the **Catalan number** (1, 1, 2, 5, 14, 42, ..., 16,796 for `n = 10`).

## Explanation

`go(prefix, opens, closes)` adds `(` while `opens < n` and `)` while `closes < opens`. When the prefix has `2n` characters it is complete and valid. Because `(` is tried first the strings come out sorted.
