---
name: sheet-median-two-sorted
title: 'Median of Two Sorted Lists'
tags: [dsa-sheet, binary-search, binary-search-on-the-answer]
difficulty: Mastery
theory: the-median
---

## Statement

`a` and `b` are each sorted in increasing order, and together they hold at least one value. Return the **median** of all their values combined, as a number with a decimal point (`3.0`, `2.5`). For an even count the median is the average of the two middle values.

Merging and sorting works, but reads everything. The big tests only allow a few hundred reads.

### Examples

**Example 1**

Input:

```python
median_two_sorted([1, 3], [2])
```

Output:

```text
2.0
```

Combined: 1, 2, 3. The median is 2.

**Example 2**

Input:

```python
median_two_sorted([1, 2], [3, 4])
```

Output:

```text
2.5
```

Combined: 1, 2, 3, 4. The median is (2 + 3) / 2 = 2.5.

### Constraints

- `1 <= len(a) + len(b) <= 4 * 10**5`
- Both lists are sorted in non-decreasing order.
- `-10**9 <= value <= 10**9`
- The big tests count how many values you read from each list.

## Explanation

Make `a` the shorter list. Binary search `i` (values taken from `a`), with `j = half - i` taken from `b`. When the four boundary values are in order (`a_left <= b_right and b_left <= a_right`) the split is right: odd total gives `max(a_left, b_left)`, even gives the mean of `max(a_left, b_left)` and `min(a_right, b_right)`. Otherwise move `hi` or `lo` depending on which side is too big.

### Complexity

- Time: O(log min(n, m)). Binary search on how many values the shorter list gives to the left half.
- Space: O(1). A few indices.
