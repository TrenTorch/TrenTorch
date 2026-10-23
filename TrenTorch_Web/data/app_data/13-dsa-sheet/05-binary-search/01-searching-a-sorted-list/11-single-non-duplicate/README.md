---
name: sheet-single-non-duplicate
title: 'The Single Element in a Sorted List'
tags: [dsa-sheet, binary-search, searching-a-sorted-list]
difficulty: Intermediate
---

## Statement

`nums` is sorted. Every value appears **exactly twice**, except for one value that appears **once**. Return that value.

### Examples

**Example 1**

Input:

```python
single_non_duplicate([1, 1, 2, 3, 3, 4, 4, 8, 8])
```

Output:

```text
2
```

**Example 2**

Input:

```python
single_non_duplicate([3, 3, 7, 7, 10, 11, 11])
```

Output:

```text
10
```

### Constraints

- `1 <= len(nums) <= 2 * 10**5 + 1`, and the length is odd
- `nums` is sorted in non-decreasing order.
- `0 <= nums[i] <= 10**9`
- The big tests count how many values your code reads from the list (the limit is stated in the failure message). Reading every value, or using `in`, `.index`, `.count`, `min` or `sorted` on the whole list, fails them.

## Theory

XOR-ing every value solves this in `O(n)`, but the list is sorted, so you can do better: `O(log n)`.

Before the single element, every pair starts at an **even** index (`0, 2, 4, ...`) and the two copies are `nums[i] == nums[i + 1]`. After the single element the pairs shift by one and start at **odd** indexes. So at a probe index `mid` (moved to an even index), the pair looks normal (`nums[mid] == nums[mid + 1]`) exactly when the single element is **to the right**.

So if `nums[mid] == nums[mid + 1]` set `lo = mid + 2`, otherwise the single element is at `mid` or to its left, `hi = mid`. The parity of the index tells you which side you are on.

## Explanation

`mid` is forced to be even. If it is paired with its right neighbour, the pairs up to there are aligned, so the single value is further right: `lo = mid + 2`. Otherwise the alignment already broke at or before `mid`: `hi = mid`. When `lo == hi` that index holds the single value.
