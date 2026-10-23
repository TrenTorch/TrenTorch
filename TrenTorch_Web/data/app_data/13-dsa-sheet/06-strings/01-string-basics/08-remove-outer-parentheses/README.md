---
name: sheet-remove-outer-parentheses
title: 'Remove Outer Parentheses'
tags: [dsa-sheet, strings, string-basics]
difficulty: Beginner
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

## Theory

Track the **depth** while scanning. A `(` that raises the depth from `0` to `1` is the **opening** parenthesis of a group; a `)` that lowers the depth from `1` to `0` is its **closing** one. Those are exactly the two characters to drop.

So: for `(`, add it to the answer only if the depth was already above `0`, then increase the depth. For `)`, decrease the depth first, then add it only if the depth is still above `0`. The order of "check" and "change" is the whole trick.

## Explanation

For `(` the current `depth` before the increase tells whether it is a group's opener (`depth == 0`); for `)` the depth after the decrease tells whether it is a closer (`depth == 0`). Everything else is kept.
