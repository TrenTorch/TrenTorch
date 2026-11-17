---
name: sheet-count-subarrays-xor-k
title: 'Subarrays With XOR K'
tags: [dsa-sheet, arrays, hard-arrays]
difficulty: Advanced
theory: prefix-xor
---

## Statement

The **XOR** of a run is all its values combined with the `^` operator. Return how many contiguous runs of `nums` have an XOR equal to `k`.

The starter code tries every start and end. It is correct but too slow. Make it fast.

### Examples

**Example 1**

Input:

```python
count_subarrays_xor_k([4, 2, 2, 6, 4], 6)
```

Output:

```text
4
```

The runs are `[4, 2]`, `[4, 2, 2, 6]`, `[2, 2, 6]` and `[6]`.

**Example 2**

Input:

```python
count_subarrays_xor_k([5, 6, 7, 8, 9], 5)
```

Output:

```text
2
```

The runs are `[5]` and `[5, 6, 7, 8, 9]`.

### Constraints

- `0 <= len(nums) <= 2 * 10**5`
- `0 <= nums[i] <= 10**9`
- `0 <= k <= 2**30`

## Explanation

`prefix` is the XOR of everything read so far. Runs ending here that XOR to `k` are those starting after an earlier prefix equal to `prefix ^ k`, and `seen` counts them. The lookup comes before recording the current prefix, as with sums.

### Complexity

- Time: O(n). One pass; the same prefix idea as for sums, using XOR.
- Space: O(n). The dictionary of prefix XOR counts.
