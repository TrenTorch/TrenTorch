---
name: sheet-basic-calculator-brackets
title: 'Calculator With Brackets'
tags: [dsa-sheet, stack-and-queue, stack-basics]
difficulty: Advanced
theory: brackets-and-minus-signs
---

## Statement

`s` is an expression with whole numbers, `+`, `-`, **round brackets** and optional spaces. `-` can also be a **minus sign in front of a bracket or a number** (`"-(2+3)"`, `"1-(-2)"`). Return the value.

For `"(1+(4+5+2)-3)+(6+8)"` the answer is `23`.

### Examples

**Example 1**

Input:

```python
calculate_brackets('(1+(4+5+2)-3)+(6+8)')
```

Output:

```text
23
```

**Example 2**

Input:

```python
calculate_brackets('1 - (-2)')
```

Output:

```text
3
```

### Constraints

- `1 <= len(s) <= 100000`
- The expression is valid.
- Every number and intermediate value fits in 64 bits.

## Explanation

`result += sign * num` is done when a number ends. The stack remembers the outside value and the sign that applies to the whole bracket.

### Complexity

- Time: O(n). One pass; each bracket pair pushes and pops once.
- Space: O(n). The stack holds one entry per open bracket.
