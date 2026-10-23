---
name: sheet-and-of-range
title: 'Bitwise AND of a Range'
tags: [dsa-sheet, bit-manipulation, bit-patterns]
difficulty: Advanced
---

## Statement

Return the bitwise AND of **every number from `left` to `right`** (both included).

The starter code ands the numbers one by one. It is correct but far too slow for big ranges.

### Examples

**Example 1**

Input:

```python
and_of_range(5, 7)
```

Output:

```text
4
```

**Example 2**

Input:

```python
and_of_range(0, 0)
```

Output:

```text
0
```

### Constraints

- `0 <= left <= right < 2**31`

## Theory

AND keeps a bit only if **every** number has it. Look at what happens to the numbers between `left` and `right`: as you count up, the low bits keep flipping from 0 to 1 and back, so any bit that changes anywhere in the range is `0` in the answer.

What survives is the **common binary prefix** of `left` and `right`: the leading bits on which they agree. The bits after the first difference all vary somewhere in the range.

So shift both numbers right until they are equal, counting the shifts, then shift the common value back left. `O(log n)` time.

## Explanation

Each shift removes the lowest bit of both numbers. When they become equal, what is left is the shared prefix, and shifting back left fills the dropped positions with zeros.
