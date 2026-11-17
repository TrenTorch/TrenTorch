---
name: sheet-range-sums
title: 'Range Sum Queries'
tags: [dsa-sheet, basics, make-it-fast]
difficulty: Intermediate
theory: prefix-sums-for-many-range-questions
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

## Explanation

`prefix = [0] + list(accumulate(nums))` gives `prefix[i] = nums[0] + ... + nums[i-1]`. The extra leading `0` makes `l = 0` work without a special case.

Each answer is `prefix[right + 1] - prefix[left]`. Total time is `O(n + q)`.

### Complexity

- Time: O(n + q). O(n) to build the prefix sums, then O(1) per query, with `q` queries.
- Space: O(n). The prefix array has `n + 1` entries (the answer list of size `q` is output, not extra work).
