---
name: sheet-repeating-and-missing
title: 'Repeating and Missing Number'
tags: [dsa-sheet, arrays, hard-arrays]
difficulty: Intermediate
theory: two-unknowns-need-two-equations
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

## Explanation

`diff = sum(nums) - n(n+1)/2 = r - m`. `square_diff = sum(x*x) - n(n+1)(2n+1)/6 = r² - m²`. Then `plus = square_diff // diff` is `r + m`, and the two values follow. `diff` is never `0` because exactly one value repeats and a different one is missing.

### Complexity

- Time: O(n). One pass for the sum and one for the sum of squares; two equations give both numbers.
- Space: O(1). A few integers.
