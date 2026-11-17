---
name: sheet-longest-subarray-sum-k-any
title: 'Longest Subarray With Sum K, Any Values'
tags: [dsa-sheet, arrays, hard-arrays]
difficulty: Advanced
theory: the-longest-run-with-any-signs
---

## Statement

Return the length of the **longest contiguous run** of `nums` that adds up to exactly `k`, or `0` if none does. Unlike the earlier version of this question, `nums` can contain **negative** values.

The starter code tries every start and end. It is correct but too slow. Make it fast.

### Examples

**Example 1**

Input:

```python
longest_subarray_sum_k_any([1, -1, 5, -2, 3], 3)
```

Output:

```text
4
```

The run `[1, -1, 5, -2]` adds to 3 and has length 4.

**Example 2**

Input:

```python
longest_subarray_sum_k_any([2, 4, 6], 5)
```

Output:

```text
0
```

No run adds to 5.

### Constraints

- `0 <= len(nums) <= 2 * 10**5`
- `-10**4 <= nums[i] <= 10**4`
- `-10**9 <= k <= 10**9`

## Explanation

`first[p]` is the earliest index whose prefix sum is `p`; `first[0] = -1` stands for the empty prefix. At index `i` with running sum `prefix`, if `prefix - k` is in `first`, the run from `first[prefix - k] + 1` to `i` adds to `k`, with length `i - first[prefix - k]`. Only record a prefix the first time it appears, to keep runs as long as possible.

### Complexity

- Time: O(n). One pass; the earliest index of each prefix sum is stored, so a lookup gives the longest subarray ending here.
- Space: O(n). The dictionary of first positions of prefix sums.
