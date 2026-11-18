---
name: sheet-kth-of-two-sorted
title: 'Kth Value of Two Sorted Lists'
tags: [dsa-sheet, binary-search, binary-search-on-the-answer]
difficulty: Mastery
theory: searching-for-the-cut
---

## Statement

`a` and `b` are each sorted in increasing order. Return the **`k`-th smallest** value of all their values combined (`k = 1` is the smallest). Equal values count separately. The big tests only allow a few hundred reads.

### Examples

**Example 1**

Input:

```python
kth_of_two_sorted([2, 3, 6, 7, 9], [1, 4, 8, 10], 5)
```

Output:

```text
6
```

Combined: 1, 2, 3, 4, 6, 7, 8, 9, 10. The 5th smallest is 6.

**Example 2**

Input:

```python
kth_of_two_sorted([1, 2], [], 2)
```

Output:

```text
2
```

### Constraints

- `1 <= k <= len(a) + len(b) <= 4 * 10**5`
- Both lists are sorted in non-decreasing order.
- `-10**9 <= value <= 10**9`
- The big tests count how many values you read from each list.

## Explanation

`a` is the shorter list. `lo = max(0, k - n)` and `hi = min(k, m)` bound how many values can come from `a`. For each `i` (and `j = k - i`) compute the four boundary values with infinities past the ends. A valid split returns `max(a_left, b_left)`; if `a_left > b_right` lower `hi`, else raise `lo`.

### Complexity

- Time: O(log min(n, m)). Binary search on how many values the shorter list gives to the first `k`.
- Space: O(1). A few indices.
