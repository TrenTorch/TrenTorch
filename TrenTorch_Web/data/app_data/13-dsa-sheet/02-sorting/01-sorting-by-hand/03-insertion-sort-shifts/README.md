---
name: sheet-insertion-sort-shifts
title: 'Insertion Sort Shifts'
tags: [dsa-sheet, sorting, sorting-by-hand]
difficulty: Beginner
---

## Statement

**Insertion sort** takes the values one at a time and slides each one left into its place among the values before it, like sorting playing cards in your hand.

```python
shifts = 0
for i in range(1, len(a)):
    key = a[i]
    j = i - 1
    while j >= 0 and a[j] > key:
        a[j + 1] = a[j]   # shift one place right
        shifts += 1
        j -= 1
    a[j + 1] = key
```

Return the final value of `shifts`: how many times a value was shifted one place to the right. Equal values do not move past each other, because the loop only shifts values that are strictly greater than `key`.

### Examples

**Example 1**

Input:

```python
insertion_sort_shifts([3, 1, 2])
```

Output:

```text
2
```

`1` shifts the `3` once, then `2` shifts the `3` once: 2 shifts.

**Example 2**

Input:

```python
insertion_sort_shifts([5, 4, 3, 2, 1])
```

Output:

```text
10
```

A reversed list of 5 has the most: 10 shifts.

### Constraints

- `0 <= len(nums) <= 2000`
- `-10**9 <= nums[i] <= 10**9`

## Theory

Insertion sort keeps the front of the list sorted. For each new value it shifts the larger values one place right until it finds the gap. It is **stable**, because it never moves equal values past each other, and it is **adaptive**: the work depends on how out of order the input is.

The number of shifts equals the number of **inversions**: pairs of positions `i < j` with `a[i] > a[j]`. Each shift fixes exactly one inversion. A sorted list has `0`, a reversed list has `n(n-1)/2`.

So insertion sort costs `O(n + inversions)`: `O(n)` on sorted data and `O(n²)` on reversed data. Nearly sorted data is its best case, which is why real libraries use it for small chunks.

## Explanation

Run the algorithm as written on a copy and count the shifts. The count is also the number of pairs `i < j` with `a[i] > a[j]`, which is what the checker compares against in a second, simpler way.
