---
name: sheet-pascal-row
title: 'A Row of Pascal's Triangle'
tags: [dsa-sheet, arrays, hard-arrays]
difficulty: Intermediate
---

## Statement

Pascal's triangle starts with row `0` equal to `[1]`. Every next row begins and ends with `1`, and each inner value is the sum of the two values above it:

```text
row 0:        1
row 1:       1 1
row 2:      1 2 1
row 3:     1 3 3 1
row 4:    1 4 6 4 1
```

Return row number `row` as a list. The values get big, and Python integers handle that exactly.

### Examples

**Example 1**

Input:

```python
pascal_row(4)
```

Output:

```text
[1, 4, 6, 4, 1]
```

**Example 2**

Input:

```python
pascal_row(0)
```

Output:

```text
[1]
```

### Constraints

- `0 <= row <= 1000`

## Theory

Building the whole triangle row by row costs `O(row²)` additions. But you only need one row, and each of its values is a **binomial coefficient**: the value at position `i` of row `r` is `C(r, i)`, the number of ways to choose `i` items from `r`.

Neighbouring coefficients are linked: `C(r, i + 1) = C(r, i) * (r - i) / (i + 1)`. So start with `C(r, 0) = 1` and compute each next value from the previous one with one multiplication and one division. That is `O(row)` big-number operations.

The division is always exact (`C(r, i + 1)` is a whole number), so use integer division `//` and multiply **before** dividing.

## Explanation

`value` starts at `1`. For each position `i` from `0` to `row`, append `value`, then update `value = value * (row - i) // (i + 1)`. Multiplying first keeps the intermediate result an exact multiple, so `//` loses nothing.
