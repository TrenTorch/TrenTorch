---
name: sheet-xor-of-range
title: 'XOR of a Range'
tags: [dsa-sheet, bit-manipulation, bit-tricks]
difficulty: Advanced
theory: xor-of-a-whole-range
---

## Statement

Return the XOR of **every number from `left` to `right`** (both included): `left ^ (left + 1) ^ ... ^ right`.

The starter code xors the numbers one by one. It is correct but far too slow for large ranges.

### Examples

**Example 1**

Input:

```python
xor_of_range(3, 9)
```

Output:

```text
2
```

**Example 2**

Input:

```python
xor_of_range(5, 5)
```

Output:

```text
5
```

### Constraints

- `0 <= left <= right <= 10**12`

## Explanation

`prefix(n)` uses the table above. Xoring the prefix up to `right` with the prefix up to `left - 1` cancels all numbers below `left`.

### Complexity

- Time: O(1). The XOR of `0..n` repeats every four values, so a prefix XOR is a table lookup and the range is the XOR of two prefixes.
- Space: O(1). Nothing is stored.
