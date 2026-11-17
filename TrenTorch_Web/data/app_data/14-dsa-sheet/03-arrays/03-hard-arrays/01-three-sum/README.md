---
name: sheet-three-sum
title: 'Three Sum'
tags: [dsa-sheet, arrays, hard-arrays]
difficulty: Advanced
theory: fix-one-squeeze-the-rest
---

## Statement

Return all the **different triples of values** from `nums` that add up to `0`. Each triple is written in increasing order, there must be no repeated triple, and the list of triples is sorted (compare the first value, then the second, then the third). A value can be used as many times as it appears in `nums`, but only at different positions.

The starter code tries every set of three positions. It is correct but too slow for long lists. Make it fast.

### Examples

**Example 1**

Input:

```python
three_sum([-1, 0, 1, 2, -1, -4])
```

Output:

```text
[[-1, -1, 2], [-1, 0, 1]]
```

The triples are `[-1, -1, 2]` and `[-1, 0, 1]`.

**Example 2**

Input:

```python
three_sum([0, 0, 0, 0])
```

Output:

```text
[[0, 0, 0]]
```

Only one different triple: `[0, 0, 0]`.

### Constraints

- `0 <= len(nums) <= 1500`
- `-10**5 <= nums[i] <= 10**5`

## Explanation

Sort, then for each `i` (skipping repeated `a[i]`) run two pointers `lo = i + 1` and `hi = n - 1`. Too small: `lo += 1`. Too big: `hi -= 1`. On a match, record the triple, step both pointers, then skip equal values at `lo` and `hi`. The triples come out in sorted order automatically because `i`, then `lo`, only move forward.

### Complexity

- Time: O(n^2). Sort once (`n log n`), then for each first value a two-pointer sweep over the rest costs O(n).
- Space: O(n). The sorted copy (the result list is extra output).
