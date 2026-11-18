---
name: sheet-k-closest-points
title: 'K Closest Points to the Origin'
tags: [dsa-sheet, heaps, heap-basics]
difficulty: Intermediate
theory: top-k-by-a-custom-key
---

## Statement

Return the `k` points of `points` that are **closest to the origin** `(0, 0)`, using the straight-line distance. Sort them by squared distance `x² + y²`, nearest first; points at the same distance go by `x` and then by `y` (increasing). Points can repeat.

For `points = [[1, 3], [-2, 2]]` and `k = 1` the answer is `[[-2, 2]]`.

### Examples

**Example 1**

Input:

```python
k_closest([[1, 3], [-2, 2]], 1)
```

Output:

```text
[[-2, 2]]
```

**Example 2**

Input:

```python
k_closest([[3, 3], [5, -1], [-2, 4]], 2)
```

Output:

```text
[[3, 3], [-2, 4]]
```

### Constraints

- `0 <= k <= len(points) <= 100000`
- `-10**4 <= x, y <= 10**4`

## Explanation

Sort order is `(squared distance, x, y)`. Pair every point with that key and run quickselect: pick a random pivot key, split into smaller keys, equal keys and larger keys, and keep going on the side that contains the `k`-th smallest. When the pool holds exactly the points that belong in the answer, sort just those `k`. Squared distances avoid square roots and floating point.

`heapq.nsmallest(k, points, key=...)` does the same with a heap in `O(n log k)`.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                                                         | Variables                                              |
| ----------------------------------------------------------------------- | ------------------------------------------------------ |
| `pool = [((p[0] * p[0] + p[1] * p[1], p[0], p[1]), p) for p in points]` | `pool = [((10, 1, 3), [1, 3]), ((8, -2, 2), [-2, 2])]` |
| `chosen = []`                                                           | `chosen = []`                                          |
| `pivot = random.choice(pool)[0]`                                        | `need = 1, pivot = (8, -2, 2)`                         |
| `less = [item for item in pool if item[0] < pivot]`                     | `less = []`                                            |
| `equal = [item for item in pool if item[0] == pivot]`                   | `equal = [((8, -2, 2), [-2, 2])]`                      |
| `chosen += equal[: need - len(less)]`                                   | `chosen = [((8, -2, 2), [-2, 2])]`                     |
| `pool = chosen`                                                         | `pool = [((8, -2, 2), [-2, 2])], need = 0`             |
| `return`                                                                | `returned = [[-2, 2]]`                                 |

### Complexity

- Time: O(n + k log k) expected. Randomised quickselect on the distance keys is expected O(n), then only the `k` chosen points are sorted.
- Space: O(n). The list of `(key, point)` pairs.
