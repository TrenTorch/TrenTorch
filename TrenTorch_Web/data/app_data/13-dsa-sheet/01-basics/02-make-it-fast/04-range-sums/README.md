---
name: sheet-range-sums
title: 'Range Sum Queries'
tags: [dsa-sheet, basics, make-it-fast]
difficulty: Intermediate
---

## Statement

Given a list `nums` and a list of `queries`, where each query `[l, r]` asks for the sum of `nums[l..r]` (both ends included), return the answer to every query in order.

The starter code adds up each range from scratch. Make it fast for many queries.

### Examples

**Example 1**

Input:

```python
range_sums([1, 2, 3, 4, 5], [[0, 4], [1, 3], [2, 2]])
```

Output:

```text
[15, 9, 3]
```

**Example 2**

Input:

```python
range_sums([-1, 5, -2], [[0, 0], [0, 2]])
```

Output:

```text
[-1, 2]
```

### Constraints

- `1 <= len(nums) <= 2 * 10**5`
- `0 <= len(queries) <= 2 * 10**5`
- `0 <= l <= r < len(nums)`
- `-10**4 <= nums[i] <= 10**4`

## Theory

Adding a range from scratch costs `O(n)` per query, so `q` queries cost `O(n q)`. With `n = q = 2 * 10⁵` that is `4 * 10¹⁰`.

A **prefix sum** array fixes this. Let `prefix[i]` be the sum of the first `i` elements. Then the sum of `nums[l..r]` is `prefix[r + 1] - prefix[l]`: everything up to `r`, minus everything before `l`. Building the array once is `O(n)`, and each query is `O(1)`. `itertools.accumulate` builds it in one call.

## Explanation

`prefix = [0] + list(accumulate(nums))` gives `prefix[i] = nums[0] + ... + nums[i-1]`. The extra leading `0` makes `l = 0` work without a special case.

Each answer is `prefix[r + 1] - prefix[l]`. Total time is `O(n + q)`.
