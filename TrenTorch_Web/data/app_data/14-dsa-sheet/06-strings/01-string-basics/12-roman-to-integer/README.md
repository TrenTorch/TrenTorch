---
name: sheet-roman-to-integer
title: 'Roman Numeral to Integer'
tags: [dsa-sheet, strings, string-basics]
difficulty: Beginner
theory: roman-numerals-to-numbers
---

## Statement

Convert a Roman numeral to a whole number. The symbols are `I = 1`, `V = 5`, `X = 10`, `L = 50`, `C = 100`, `D = 500`, `M = 1000`. Normally symbols are written from the largest to the smallest and added, but a smaller symbol **before** a bigger one is **subtracted**: `IV = 4`, `IX = 9`, `XL = 40`, `XC = 90`, `CD = 400`, `CM = 900`.

### Examples

**Example 1**

Input:

```python
roman_to_integer('III')
```

Output:

```text
3
```

Three ones.

**Example 2**

Input:

```python
roman_to_integer('MCMXCIV')
```

Output:

```text
1994
```

1000 + 900 + 90 + 4 = 1994.

### Constraints

- `1 <= len(s) <= 15`
- `s` is a valid Roman numeral (a number from 1 to 3999) made of the seven symbols.

## Explanation

`values` maps each symbol to its number. For each position, if the next symbol is bigger the current one is subtracted, otherwise added. The last symbol is added.

### Complexity

- Time: O(n). One pass; a symbol smaller than the next one is subtracted.
- Space: O(1). A fixed table of seven symbols.
