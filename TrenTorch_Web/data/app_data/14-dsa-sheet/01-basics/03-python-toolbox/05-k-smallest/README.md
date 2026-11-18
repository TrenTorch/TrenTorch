---
name: sheet-k-smallest
title: 'K Smallest Numbers'
tags: [dsa-sheet, basics, python-toolbox]
difficulty: Beginner
theory: heaps-and-merging
---

## Statement

Return the `k` smallest numbers of `nums` in increasing order. If `k` is larger than the list, return all of them sorted. Equal values count separately.

### Examples

**Example 1**

Input:

```python
k_smallest([7, 2, 9, 4, 2], 3)
```

Output:

```text
[2, 2, 4]
```

**Example 2**

Input:

```python
k_smallest([5, 1], 10)
```

Output:

```text
[1, 5]
```

### Constraints

- `0 <= len(nums) <= 3 * 10**5`
- `0 <= k <= 3 * 10**5`
- `-10**9 <= nums[i] <= 10**9`

## Explanation

Quickselect. Pick a random pivot and split the pool into `less`, `equal` and `greater`. If all `k` wanted values lie inside `less`, continue with `less` only. If they reach into the `equal` block, take all of `less` and just enough copies of the pivot. Otherwise keep all of `less` and `equal` and continue with `greater` for the rest.

The pool shrinks by a constant factor on average, so the total work is a geometric series, `O(n)`. Only the `k` chosen values are sorted at the end, which is why equal values and `k >= len(nums)` need no special handling beyond the early return.

`heapq.nsmallest(k, nums)` is the short alternative: `O(n log k)` time and `O(k)` space.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                           | Variables                      |
| ----------------------------------------- | ------------------------------ |
| `chosen = []`                             | `chosen = []`                  |
| `pool = list(nums)`                       | `pool = [7, 2, 9, 4, 2]`       |
| `pivot = random.choice(pool)`             | `need = 3, pivot = 4`          |
| `less = [x for x in pool if x < pivot]`   | `less = [2, 2]`                |
| `equal = [x for x in pool if x == pivot]` | `equal = [4]`                  |
| `chosen += less`                          | `chosen = [2, 2]`              |
| `need = 0`                                | `chosen = [2, 2, 4], need = 0` |
| `return`                                  | `returned = [2, 2, 4]`         |

### Complexity

- Time: O(n + k log k) expected. Randomised quickselect shrinks the pool geometrically (expected O(n) work in total) and only the `k` chosen values are sorted.
- Space: O(n). The working pool; a heap instead would trade time `O(n log k)` for space `O(k)`.
