---
name: sheet-count-pairs
title: 'Count the Pairs'
tags: [dsa-sheet, basics, counting-steps]
difficulty: Beginner
theory: pairs-and-the-staircase
---

## Statement

This code counts pairs of positions:

```python
count = 0
for i in range(n):
    for j in range(i + 1, n):
        count += 1
```

Implement `count_pairs(n)` so it returns the final value of `count`.

`n` can be huge, so you cannot run the loops. Work the number out from the shape of the loops.

### Examples

**Example 1**

Input:

```python
count_pairs(4)
```

Output:

```text
6
```

The pairs are (0,1) (0,2) (0,3) (1,2) (1,3) (2,3).

**Example 2**

Input:

```python
count_pairs(1)
```

Output:

```text
0
```

No pair fits.

### Constraints

- `0 <= n <= 10**12`
- Your function must answer instantly, even for the largest `n`.

## Explanation

The inner loop runs `n-1-i` times for each `i`, so the total is the sum of `0..n-1`, which is `n(n-1)/2`.

`n * (n - 1)` is always even (one of two neighbours is even), so `//` gives the exact answer. Python integers do not overflow, so `10**12` squared is fine.

### Complexity

- Time: O(1). One multiplication, one subtraction and one division on a number that fits in a machine word.
- Space: O(1). Nothing is stored besides the input and the result.
