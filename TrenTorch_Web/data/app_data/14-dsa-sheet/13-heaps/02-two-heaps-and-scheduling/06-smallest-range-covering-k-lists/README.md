---
name: sheet-smallest-range-covering-k-lists
title: 'Smallest Range Covering K Lists'
tags: [dsa-sheet, heaps, two-heaps-and-scheduling]
difficulty: Mastery
theory: moving-the-smallest-forward
---

## Statement

`lists` holds `k` lists of numbers, each sorted in increasing order and non-empty. Find the **smallest range `[lo, hi]`** that contains **at least one number from every list**. A range `[a, b]` is smaller than `[c, d]` if `b - a < d - c`, or if the lengths are equal and `a < c`. Return `[lo, hi]`.

For `[[4, 10, 15, 24, 26], [0, 9, 12, 20], [5, 18, 22, 30]]` the answer is `[20, 24]`.

### Examples

**Example 1**

Input:

```python
smallest_range([[4, 10, 15, 24, 26], [0, 9, 12, 20], [5, 18, 22, 30]])
```

Output:

```text
[20, 24]
```

**Example 2**

Input:

```python
smallest_range([[1, 2, 3], [1, 2, 3], [1, 2, 3]])
```

Output:

```text
[1, 1]
```

### Constraints

- `1 <= k <= 3500`
- `1 <= total number of values <= 100000`
- `-10**5 <= value <= 10**5`

## Explanation

The heap stores `(value, list_index, position)`. `current_max` is the largest value currently chosen. When any list is exhausted, no range can cover all lists any more.

### Complexity

- Time: O(N log k). A heap with one value per list; each of the `N` values is pushed and popped at most once.
- Space: O(k). The heap.
