---
name: sheet-zigzag-conversion
title: 'Zigzag Conversion'
tags: [dsa-sheet, strings, harder-strings]
difficulty: Intermediate
---

## Statement

Write the characters of `s` in a **zigzag** pattern over `rows` rows: go down the rows one character at a time, then back up diagonally, and repeat. Then read the result **row by row**, left to right, top to bottom.

For `s = "PAYPALISHIRING"` and `rows = 3`:

```text
P   A   H   N
A P L S I I G
Y   I   R
```

which reads `"PAHNAPLSIIGYIR"`. With one row the string is unchanged.

### Examples

**Example 1**

Input:

```python
zigzag_conversion('PAYPALISHIRING', 3)
```

Output:

```text
'PAHNAPLSIIGYIR'
```

The three rows read `PAHN`, `APLSIIG`, `YIR`.

**Example 2**

Input:

```python
zigzag_conversion('PAYPALISHIRING', 4)
```

Output:

```text
'PINALSIGYAHRPI'
```

The four rows read `PIN`, `ALSIG`, `YAHR`, `PI`.

### Constraints

- `0 <= len(s) <= 3 * 10**5`
- `1 <= rows <= 1000`

## Theory

You do not need to draw the grid. Think of the **row index** each character lands on: it goes `0, 1, 2, ..., rows - 1`, then `rows - 2, ..., 1`, then `0` again, bouncing between the first and last row.

So keep a list of `rows` strings (or lists). For each character, append it to the row at the current index, then move the index by `+1` or `-1`, reversing direction when you reach the first or last row. Finally join the rows. This is a simulation in `O(n)`.

With a single row the index can neither go up nor down, so handle `rows == 1` (or `rows >= len(s)`) separately: the answer is `s` itself.

## Explanation

`lines` holds one list per row. `row` is the current row and `step` is `+1` or `-1`. After placing a character, flip `step` when `row` is `0` or `rows - 1`, then move. Joining all rows gives the row-by-row reading.
