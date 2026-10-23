---
name: sheet-count-reverse-pairs
title: 'Count Reverse Pairs'
tags: [dsa-sheet, arrays, hard-arrays]
difficulty: Advanced
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

## Theory

This is **Count Inversions** with a different rule, and the same merge sort idea solves it. Split the list, solve each half, and then count the pairs that have `i` in the left half and `j` in the right half.

Here is the catch: the counting condition (`left > 2 * right`) is not the same as the merge condition (`left > right`), so you count in a **separate pass before merging**. Both halves are already sorted, so walk the left half in increasing order while a pointer `j` moves through the right half: as the left value grows, more right values satisfy `left > 2 * right`, so `j` never moves backwards. Add `j` for each left value. Then merge (or just sort) the two halves and return.

Each level does `O(n)` work and there are `log₂ n` levels: `O(n log n)`.

## Explanation

`sort(a)` returns the sorted list and the number of reverse pairs. After sorting both halves, for each `v` in `left` (increasing), advance `j` while `v > 2 * right[j]` and add `j`. Then `sorted(left + right)` merges the halves; Python's sort detects the two sorted runs, so this step is linear.
