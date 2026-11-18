---
name: sheet-count-doubling-steps
title: 'Doubling Steps'
tags: [dsa-sheet, basics, counting-steps]
difficulty: Beginner
theory: doubling-is-halving-in-reverse
---

## Statement

This loop doubles `i` until it reaches `n`:

```python
count = 0
i = 1
while i < n:
    i *= 2
    count += 1
```

Implement `count_doubling_steps(n)` so it returns the final value of `count`.

### Examples

**Example 1**

Input:

```python
count_doubling_steps(8)
```

Output:

```text
3
```

`i` goes 1, 2, 4, 8.

**Example 2**

Input:

```python
count_doubling_steps(9)
```

Output:

```text
4
```

`i` goes 1, 2, 4, 8, 16.

### Constraints

- `1 <= n <= 10**18`

## Explanation

After `k` rounds `i = 2**k`. The loop stops at the first `k` with `2**k >= n`, which is `ceil(log₂ n)`.

`(n - 1).bit_length()` computes exactly that with integers. A float `math.log2` would round wrong near powers of two for large `n`.

### Complexity

- Time: O(1). `bit_length()` of `n - 1` replaces a loop of about `log2(n)` doublings.
- Space: O(1). A single integer is produced.
