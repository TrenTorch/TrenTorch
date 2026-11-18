---
name: sheet-pascal-row
title: 'A Row of Pascal's Triangle'
tags: [dsa-sheet, arrays, hard-arrays]
difficulty: Intermediate
theory: a-row-of-pascal-s-triangle
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

## Explanation

`value` starts at `1`. For each position `i` from `0` to `row`, append `value`, then update `value = value * (row - i) // (i + 1)`. Multiplying first keeps the intermediate result an exact multiple, so `//` loses nothing.

### Complexity

- Time: O(row). `row + 1` steps, each one multiplication and one division of numbers with at most `row` bits.
- Space: O(row). The result list holds `row + 1` numbers.
