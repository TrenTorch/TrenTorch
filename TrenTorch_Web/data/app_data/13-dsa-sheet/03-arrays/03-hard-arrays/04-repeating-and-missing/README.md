---
name: sheet-repeating-and-missing
title: 'Repeating and Missing Number'
tags: [dsa-sheet, arrays, hard-arrays]
difficulty: Intermediate
---

## Statement

`nums` has `n` values and should contain every number from `1` to `n` exactly once, but one number appears **twice** and another is **missing**. Return `[repeated, missing]`.

### Examples

**Example 1**

Input:

```python
repeating_and_missing([3, 1, 2, 5, 3])
```

Output:

```text
[3, 4]
```

`3` appears twice and `4` is missing.

**Example 2**

Input:

```python
repeating_and_missing([1, 1])
```

Output:

```text
[1, 2]
```

`1` appears twice and `2` is missing.

### Constraints

- `2 <= len(nums) <= 2 * 10**5`
- Every value is between `1` and `len(nums)`.
- Exactly one value repeats and exactly one is missing.

## Theory

A set or a counting list solves it in `O(n)` with `O(n)` memory. With **maths** you can do it in `O(1)` memory.

Let `r` be the repeated value and `m` the missing one. Compare the list with the ideal `1..n`: the **sums** differ by `r - m`, and the **sums of squares** differ by `r² - m²`. From the second, `r² - m² = (r - m)(r + m)`, so once you know `r - m` you get `r + m` by division. Then `r = ((r + m) + (r - m)) / 2` and `m = ((r + m) - (r - m)) / 2`.

Two equations, two unknowns: a small algebra trick that turns a search problem into arithmetic.

## Explanation

`diff = sum(nums) - n(n+1)/2 = r - m`. `square_diff = sum(x*x) - n(n+1)(2n+1)/6 = r² - m²`. Then `plus = square_diff // diff` is `r + m`, and the two values follow. `diff` is never `0` because exactly one value repeats and a different one is missing.
