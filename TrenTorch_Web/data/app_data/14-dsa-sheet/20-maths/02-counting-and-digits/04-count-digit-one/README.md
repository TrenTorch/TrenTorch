---
name: sheet-count-digit-one
title: 'Count the Digit One'
tags: [dsa-sheet, maths, counting-and-digits]
difficulty: Mastery
theory: counting-the-digit-one
---

## Statement

Return the **total number of times the digit `1` appears** when you write all the numbers from `1` to `n`.

For `n = 13` the answer is `6` (`1, 10, 11` (two), `12, 13`).

The starter code looks at the digits of every number. It is correct but too slow for large `n`.

### Examples

**Example 1**

Input:

```python
count_digit_one(13)
```

Output:

```text
6
```

**Example 2**

Input:

```python
count_digit_one(0)
```

Output:

```text
0
```

### Constraints

- `0 <= n <= 9 * 10**15`

## Explanation

`high * p` counts the full blocks; the `if/elif` adds the partial block depending on the current digit.

### Complexity

- Time: O(log n). One step per digit position, each a constant number of divisions.
- Space: O(1). A few integers.
