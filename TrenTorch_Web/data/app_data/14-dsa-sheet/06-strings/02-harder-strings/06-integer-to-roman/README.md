---
name: sheet-integer-to-roman
title: 'Integer to Roman Numeral'
tags: [dsa-sheet, strings, harder-strings]
difficulty: Intermediate
theory: numbers-to-roman-numerals
---

## Statement

Convert `num` to a Roman numeral. The symbols are `I = 1`, `V = 5`, `X = 10`, `L = 50`, `C = 100`, `D = 500`, `M = 1000`. Symbols are written from the largest to the smallest and added, except for these six **subtractive** forms: `IV = 4`, `IX = 9`, `XL = 40`, `XC = 90`, `CD = 400`, `CM = 900`.

### Examples

**Example 1**

Input:

```python
integer_to_roman(3)
```

Output:

```text
'III'
```

`III`.

**Example 2**

Input:

```python
integer_to_roman(1994)
```

Output:

```text
'MCMXCIV'
```

`M` + `CM` + `XC` + `IV`.

### Constraints

- `1 <= num <= 3999`

## Explanation

`table` lists values from largest to smallest with their symbols, including the nine/four forms. For each value, `divmod(num, value)` gives how many times it fits; append the symbol that many times and continue with the remainder.

### Complexity

- Time: O(1). A fixed table of 13 symbols; the output has at most 15 characters.
- Space: O(1). The output is bounded.
