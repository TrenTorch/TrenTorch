---
name: sheet-sparse-table
title: 'Sparse Table (Static Range Minimum)'
tags: [dsa-sheet, design, range-structures]
difficulty: Advanced
theory: two-overlapping-blocks
---

## Statement

`nums` never changes. Each query `[l, r]` asks for the **smallest value in `nums[l..r]`** (both ends included). Return the answers in order.

For `nums = [5, 2, 8, 1, 9]` and `queries = [[0, 4], [1, 2], [2, 2]]` the answer is `[1, 2, 8]`.

The starter code scans the range for each query. It is correct but too slow for many queries.

### Examples

**Example 1**

Input:

```python
range_minimums([5, 2, 8, 1, 9], [[0, 4], [1, 2], [2, 2]])
```

Output:

```text
[1, 2, 8]
```

**Example 2**

Input:

```python
range_minimums([3], [[0, 0]])
```

Output:

```text
[3]
```

### Constraints

- `1 <= len(nums) <= 65536`
- `0 <= len(queries) <= 100000`
- `0 <= l <= r < len(nums)`
- `-10**9 <= nums[i] <= 10**9`

## Explanation

`(r - l + 1).bit_length() - 1` is `floor(log2(length))`. The two table entries cover the range from both ends.

### Complexity

- Time: O(n log n + q). The table has `log n` rows of up to `n` minimums, and each query overlaps two precomputed ranges, so it is O(1).
- Space: O(n log n). The table.
