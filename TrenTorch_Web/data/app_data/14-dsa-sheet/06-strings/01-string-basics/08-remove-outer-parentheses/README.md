---
name: sheet-remove-outer-parentheses
title: 'Remove Outer Parentheses'
tags: [dsa-sheet, strings, string-basics]
difficulty: Beginner
theory: using-the-counter-to-decide-what-to-keep
---

## Statement

`s` is a valid string made only of `(` and `)`. Split it into **primitive groups**: the shortest non-empty balanced pieces, such as `()` and `(())`, read from left to right. Remove the outermost parentheses of **every** group and join what is left.

For example `"(()())(())"` is the groups `(()())` and `(())`, which become `()()` and `()`: the answer is `"()()()"`.

### Examples

**Example 1**

Input:

```python
remove_outer_parentheses('(()())(())')
```

Output:

```text
'()()()'
```

**Example 2**

Input:

```python
remove_outer_parentheses('()()')
```

Output:

```text
''
```

### Constraints

- `0 <= len(s) <= 3 * 10**5`
- `s` is balanced and contains only `(` and `)`.

## Explanation

For `(` the current `depth` before the increase tells whether it is a group's opener (`depth == 0`); for `)` the depth after the decrease tells whether it is a closer (`depth == 0`). Everything else is kept.

### Complexity

- Time: O(n). One pass tracking the depth.
- Space: O(n). The result string.
