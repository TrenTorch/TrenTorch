---
name: sheet-min-flips-to-make-or
title: 'Minimum Flips to Make a OR b Equal c'
tags: [dsa-sheet, bit-manipulation, bit-patterns]
difficulty: Intermediate
theory: flips-needed-so-a-or-b-equals-c
---

## Statement

Return the **minimum number of bit flips** in `a` and `b` (a flip changes one bit of one of them) so that `a | b == c`.

For `a = 2`, `b = 6`, `c = 5` the answer is `3`.

### Examples

**Example 1**

Input:

```python
min_flips(2, 6, 5)
```

Output:

```text
3
```

**Example 2**

Input:

```python
min_flips(4, 2, 7)
```

Output:

```text
1
```

### Constraints

- `0 <= a, b, c < 2**31`

## Explanation

The loop runs over bit positions and applies the case analysis above. Positions where `a | b` already equals `c` cost nothing.

### Complexity

- Time: O(1). Each of the 31 bit positions is checked once.
- Space: O(1). A few integers.
