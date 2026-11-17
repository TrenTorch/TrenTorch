---
name: sheet-nth-digit
title: 'The Nth Digit'
tags: [dsa-sheet, maths, counting-and-digits]
difficulty: Advanced
theory: the-nth-digit-of-an-endless-string
---

## Statement

Write all the positive whole numbers one after another: `123456789101112131415...`. Return the **`n`-th digit** of this endless string (counting from 1).

For `n = 11` the answer is `0` (the digits are `1 2 3 4 5 6 7 8 9 1 0 1 1 ...`).

The starter code writes the numbers until the text is long enough. It is correct but too slow, and uses too much memory, for large `n`.

### Examples

**Example 1**

Input:

```python
nth_digit(11)
```

Output:

```text
0
```

**Example 2**

Input:

```python
nth_digit(3)
```

Output:

```text
3
```

### Constraints

- `1 <= n <= 9 * 10**15`

## Explanation

The loop skips whole groups. Then integer division finds the number and the remainder finds the position inside it.

### Complexity

- Time: O(log n). Skipping whole blocks of 1-digit, 2-digit, ... numbers takes one step per digit length.
- Space: O(1). A few integers.
