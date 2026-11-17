---
name: sheet-count-reverse-pairs
title: 'Count Reverse Pairs'
tags: [dsa-sheet, arrays, hard-arrays]
difficulty: Advanced
theory: a-different-pair-condition
---

## Statement

A **reverse pair** is a pair of positions `i < j` with `nums[i] > 2 * nums[j]`. Count them.

The starter code checks every pair. It is correct but too slow for long lists. Make it fast.

### Examples

**Example 1**

Input:

```python
count_reverse_pairs([1, 3, 2, 3, 1])
```

Output:

```text
2
```

The pairs are `(3, 1)` at positions 1, 4 and `(3, 1)` at positions 3, 4.

**Example 2**

Input:

```python
count_reverse_pairs([2, 4, 3, 5, 1])
```

Output:

```text
3
```

The pairs are `(4, 1)`, `(3, 1)` and `(5, 1)`.

### Constraints

- `0 <= len(nums) <= 5 * 10**4`
- `-10**9 <= nums[i] <= 10**9`

## Explanation

`sort(a)` returns the sorted list and the number of reverse pairs. After sorting both halves, for each `v` in `left` (increasing), advance `j` while `v > 2 * right[j]` and add `j`. Then `sorted(left + right)` merges the halves; Python's sort detects the two sorted runs, so this step is linear.

### Complexity

- Time: O(n log n). Merge sort has `log n` levels; at each level the pairs are counted with two pointers and the halves are merged in linear time.
- Space: O(n). The merged lists along the recursion path add up to `n`.
