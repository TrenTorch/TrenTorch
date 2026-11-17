---
name: sheet-kth-largest
title: 'Kth Largest Value'
tags: [dsa-sheet, sorting, divide-and-conquer]
difficulty: Intermediate
theory: k-th-largest-and-the-cost
---

## Statement

Return the `k`-th largest value in `nums`, where `k = 1` is the largest. Equal values count separately: in `[5, 5, 3]` the 2nd largest is `5` and the 3rd largest is `3`.

Sorting the whole list works, but you only need one value. See if you can do it faster.

### Examples

**Example 1**

Input:

```python
kth_largest([3, 2, 1, 5, 6, 4], 2)
```

Output:

```text
5
```

Sorted from largest: 6, 5, 4, 3, 2, 1. The 2nd is 5.

**Example 2**

Input:

```python
kth_largest([5, 5, 3], 3)
```

Output:

```text
3
```

Sorted from largest: 5, 5, 3. The 3rd is 3.

### Constraints

- `1 <= k <= len(nums) <= 2 * 10**5`
- `-10**9 <= nums[i] <= 10**9`

## Explanation

Convert to an ascending index: the `k`-th largest is at index `len - k` in sorted order. Pick a random value as pivot and split into `less`, the `equal` count, and `greater`. If the target index is inside `less`, loop on `less`. If it is inside the equal block, return the pivot. Otherwise subtract the sizes of `less` and the equal block from the target and loop on `greater`.

A random pivot keeps the expected work linear whatever the input order; a fixed pivot such as the middle element can be pushed to `O(n^2)` by a crafted input.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                      | Variables                |
| ------------------------------------ | ------------------------ |
| `a = list(nums)`                     | `a = [3, 2, 1, 5, 6, 4]` |
| `target = len(a) - k`                | `target = 4`             |
| `pivot = random.choice(a)`           | `pivot = 5`              |
| `less = [x for x in a if x < pivot]` | `less = [3, 2, 1, 4]`    |
| `equal = a.count(pivot)`             | `equal = 1`              |
| `return`                             | `returned = 5`           |

### Complexity

- Time: O(n) expected. A random pivot keeps the pool about 3/4 of its size on average, so the work is a geometric series `n + 3n/4 + ...`.
- Space: O(n). The working pool of values.
