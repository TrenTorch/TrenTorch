---
name: sheet-zigzag-conversion
title: 'Zigzag Conversion'
tags: [dsa-sheet, strings, harder-strings]
difficulty: Intermediate
theory: bouncing-up-and-down
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

## Explanation

`lines` holds one list per row. `row` is the current row and `step` is `+1` or `-1`. After placing a character, flip `step` when `row` is `0` or `rows - 1`, then move. Joining all rows gives the row-by-row reading.

### Complexity

- Time: O(n). Each character is placed in its row once.
- Space: O(n). The row lists hold every character.
