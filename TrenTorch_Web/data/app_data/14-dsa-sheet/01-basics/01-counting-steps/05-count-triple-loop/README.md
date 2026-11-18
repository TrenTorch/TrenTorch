---
name: sheet-count-triple-loop
title: 'Three Nested Loops'
tags: [dsa-sheet, basics, counting-steps]
difficulty: Intermediate
theory: three-nested-loops
---

## Statement

This code has three loops that each start where the previous one is:

```python
count = 0
for i in range(n):
    for j in range(i, n):
        for k in range(j, n):
            count += 1
```

Implement `count_triple_loop(n)` so it returns the final value of `count`.

### Examples

**Example 1**

Input:

```python
count_triple_loop(3)
```

Output:

```text
10
```

The triples are (0,0,0) (0,0,1) (0,0,2) (0,1,1) (0,1,2) (0,2,2) (1,1,1) (1,1,2) (1,2,2) (2,2,2).

**Example 2**

Input:

```python
count_triple_loop(5)
```

Output:

```text
35
```

### Constraints

- `0 <= n <= 10**6`

## Explanation

The count is the number of triples `i <= j <= k` taken from `0..n-1`. That is the number of multisets of size 3 from `n` items, which is `C(n+2, 3) = n(n+1)(n+2)/6`.

The product of three consecutive integers is divisible by 6, so `//` is exact.

### Complexity

- Time: O(1). The answer is the closed form `n(n+1)(n+2)/6`: three multiplications and one division.
- Space: O(1). A single integer is produced.
