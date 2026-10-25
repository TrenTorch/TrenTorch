---
name: sheet-nth-root
title: 'Integer Root'
tags: [dsa-sheet, binary-search, binary-search-on-the-answer]
difficulty: Intermediate
---

## Statement

Return the whole number `x` such that `x ** m == n`, or `-1` if there is no such whole number.

For example the cube root of `27` is `3`, and `2` has no whole square root, so the answer is `-1`.

### Examples

**Example 1**

Input:

```python
nth_root(27, 3)
```

Output:

```text
3
```

**Explanation:** Cube root of 27 equals 3 because 3**3 equals 27.

**Example 2**

Input:

```python
nth_root(2, 2)
```

Output:

```text
-1
```

**Explanation:** No integer square root of 2 exists, so function returns -1.

### Constraints

- `1 <= n <= 10**18`
- `1 <= m <= 40`
- Trying every `x` one by one is too slow for the large tests.

## Theory

You are searching for a number `x` between `1` and `n`, and you have a way to test any guess: compute `x ** m` and compare it with `n`. Because `x ** m` **grows with `x`**, a guess that is too big stays too big for bigger guesses. That is exactly the situation binary search works in, even though there is no list: the "list" is the range of possible answers.

Keep `lo = 1`, `hi = n`. Try `mid`. If `mid ** m == n` you found it. If it is smaller, search higher; if bigger, search lower. For `n = 10¹⁸` this takes about 60 guesses instead of up to a billion.

This idea, **binary search on the answer**, is the key tool of the whole second half of this topic: whenever the answer is a number in a range and you can check "is this guess big enough?", you can binary search it.

## Explanation

The guess range starts at `[1, n]` (the root is never above `n`). The comparison of `mid ** m` with `n` decides which half to keep. If the loop finishes without an exact match, no whole root exists and the answer is `-1`. Python integers do not overflow, so `mid ** m` is exact even for big values.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line        | Variables               |
| ---------------------- | ----------------------- |
| `lo, hi = 1, n`        | `lo = 1, hi = 27`       |
| `mid = (lo + hi) // 2` | `mid = 14`              |
| `hi = mid - 1`         | `hi = 13, power = 2744` |
| `mid = (lo + hi) // 2` | `mid = 7`               |
| `power = mid**m`       | `power = 343`           |
| `hi = mid - 1`         | `hi = 6`                |
| `power = mid**m`       | `mid = 3, power = 27`   |
| `return`               | `returned = 3`          |
