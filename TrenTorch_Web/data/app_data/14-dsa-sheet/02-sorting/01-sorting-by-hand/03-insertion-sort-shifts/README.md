---
name: sheet-insertion-sort-shifts
title: 'Insertion Sort Shifts'
tags: [dsa-sheet, sorting, sorting-by-hand]
difficulty: Beginner
theory: counting-the-shifts
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

## Explanation

Each shift moves one bigger value past `key`, which removes exactly one pair `i < j` with `a[i] > a[j]`. So the number of shifts is the number of such pairs (inversions).

A Fenwick tree over the ranks of the values counts, for every element, how many earlier values are bigger: `seen - (earlier values that are not bigger)`. Running the algorithm as written on a copy and counting the shifts also works at this size, in `O(n^2)`.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                                              | Variables                                                    |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| `rank = {v: i + 1 for i, v in enumerate(sorted(set(nums)))}` | `rank = {1: 1, 2: 2, 3: 3}`                                  |
| `for seen, x in enumerate(nums):`                            | `size = 3, tree = [0, 0, 0, 0], shifts = 0, seen = 0, x = 3` |
| `i -= i & -i`                                                | `i = 0, not_bigger = 0`                                      |
| `for seen, x in enumerate(nums):`                            | `tree = [0, 0, 0, 1], seen = 1, x = 1, i = 4`                |
| `tree[i] += 1`                                               | `tree = [0, 1, 0, 1], shifts = 1, i = 1`                     |
| `for seen, x in enumerate(nums):`                            | `tree = [0, 1, 1, 1], seen = 2, x = 2, i = 4`                |
| `shifts += seen - not_bigger`                                | `shifts = 2, i = 0, not_bigger = 1`                          |
| `return`                                                     | `returned = 2`                                               |

### Complexity

- Time: O(n log n). Every shift removes exactly one inversion, so the answer is the number of inversions, and a Fenwick tree counts them in `log n` per element.
- Space: O(n). The Fenwick tree and the rank table.
