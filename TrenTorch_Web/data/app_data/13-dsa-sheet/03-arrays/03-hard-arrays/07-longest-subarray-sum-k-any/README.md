---
name: sheet-longest-subarray-sum-k-any
title: 'Longest Subarray With Sum K, Any Values'
tags: [dsa-sheet, arrays, hard-arrays]
difficulty: Advanced
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

## Theory

With negative values the sliding window fails (the sum can go down as the window grows). Use **prefix sums** again. The run between prefix positions `a < b` has sum `prefix[b] - prefix[a]`. It equals `k` when `prefix[a] = prefix[b] - k`.

To make the run **as long as possible**, you want the **earliest** position `a` with that prefix value. So store, in a dictionary, the **first index** where each prefix sum occurred (and never overwrite it). At each position look up `prefix - k` and update the best length `b - a`. Start with `{0: -1}` for the empty prefix before the first value.

It is the same dictionary trick as counting runs, but you store the first index instead of a count.

## Explanation

`first[p]` is the earliest index whose prefix sum is `p`; `first[0] = -1` stands for the empty prefix. At index `i` with running sum `prefix`, if `prefix - k` is in `first`, the run from `first[prefix - k] + 1` to `i` adds to `k`, with length `i - first[prefix - k]`. Only record a prefix the first time it appears, to keep runs as long as possible.
