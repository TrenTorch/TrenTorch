---
name: sheet-integer-to-roman
title: 'Integer to Roman Numeral'
tags: [dsa-sheet, strings, harder-strings]
difficulty: Intermediate
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

## Theory

This is a **greedy** algorithm: always take the biggest value that still fits. Make a table of the values in decreasing order **including the six subtractive pairs**: `1000 M`, `900 CM`, `500 D`, `400 CD`, `100 C`, `90 XC`, `50 L`, `40 XL`, `10 X`, `9 IX`, `5 V`, `4 IV`, `1 I`.

Walk down the table. While the number is at least the current value, append its symbol and subtract the value. Putting the subtractive pairs in the table is what makes greedy correct: without `IV` the greedy choice for 4 would be `IIII`.

Greedy works here because each value in the table is not too far from the next, so taking the largest never blocks a better answer later. It is worth checking, not assuming, that greedy works for a given coin system.

## Explanation

`table` lists values from largest to smallest with their symbols, including the nine/four forms. For each value, `divmod(num, value)` gives how many times it fits; append the symbol that many times and continue with the remainder.
