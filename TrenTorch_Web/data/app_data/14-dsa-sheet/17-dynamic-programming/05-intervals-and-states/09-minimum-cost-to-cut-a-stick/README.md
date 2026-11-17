---
name: sheet-minimum-cost-to-cut-a-stick
title: 'Minimum Cost to Cut a Stick'
tags: [dsa-sheet, dynamic-programming, intervals-and-states]
difficulty: Mastery
theory: burst-balloons-and-cutting-a-stick
---

## Statement

A stick of length `length` must be cut at the positions in `cuts`, in any order you choose. The cost of one cut is the **current length of the piece being cut**. Return the **smallest total cost**.

For `length = 7` and `cuts = [1, 3, 4, 5]` the answer is `16` (cut at 3, then 5, then 1, then 4: costs 7 + 4 + 3 + 2).

The starter code tries every order of the cuts. It is correct but too slow for many cuts.

### Examples

**Example 1**

Input:

```python
min_cost_cut(7, [1, 3, 4, 5])
```

Output:

```text
16
```

**Example 2**

Input:

```python
min_cost_cut(9, [5, 6, 1, 4, 2])
```

Output:

```text
22
```

### Constraints

- `2 <= length <= 1000000`
- `0 <= len(cuts) <= 100`
- `1 <= cut < length`, all different

## Explanation

Add the two ends to the cut points and sort. `dp[i][j]` is the cheapest way to make all cuts strictly between points `i` and `j`: choose the first cut `k` there, pay the length `points[j] - points[i]`, and solve the two halves.

Trying every `k` makes `O(m^3)`. But the best `k` for `(i, j)` never lies left of the best `k` for `(i, j - 1)` nor right of the best `k` for `(i + 1, j)` (Knuth's optimisation). Remember the best `k` of each cell and only search between those two, and the searches along each diagonal add up to `O(m)`.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                          | Variables                                                                                                                                                                                                    |
| ---------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `points = [0] + sorted(cuts) + [length]` | `points = [0, 1, 3, 4, 5, 7]`                                                                                                                                                                                |
| `low = max(i + 1, best_cut[i][j - 1])`   | `n = 6, dp = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, ..., best_cut = [[0, 1, 0, 0, 0, 0], [0, 0, 2, 0, 0, 0], [0, 0, 0, 3, 0, ..., i = 0, span = 2, j = 2, low = 1`                         |
| `for i in range(n - span):`              | `dp = [[0, 0, 3, 0, 0, 0], [0, 0, 0, 3, 0, 0], [0, 0, 0, 0, 0, ..., best_cut = [[0, 1, 1, 0, 0, 0], [0, 0, 2, 2, 0, 0], [0, 0, 0, 3, 0, ..., i = 2, j = 3, low = 2, high = 2, best = 0, k = 2, value = 0`    |
| `for span in range(2, n):`               | `dp = [[0, 0, 3, 0, 0, 0], [0, 0, 0, 3, 0, 0], [0, 0, 0, 0, 2, ..., best_cut = [[0, 1, 1, 0, 0, 0], [0, 0, 2, 2, 0, 0], [0, 0, 0, 3, 3, ..., i = 3, span = 3, j = 5, low = 4, high = 4, k = 4`               |
| `value = dp[i][k] + dp[k][j]`            | `dp = [[0, 0, 3, 7, 0, 0], [0, 0, 0, 3, 0, 0], [0, 0, 0, 0, 2, ..., best_cut = [[0, 1, 1, 1, 0, 0], [0, 0, 2, 2, 0, 0], [0, 0, 0, 3, 3, ..., i = 1, j = 4, low = 2, high = 3, best = None, k = 2, value = 2` |
| `for i in range(n - span):`              | `dp = [[0, 0, 3, 7, 0, 0], [0, 0, 0, 3, 6, 0], [0, 0, 0, 0, 2, ..., best_cut = [[0, 1, 1, 1, 0, 0], [0, 0, 2, 2, 2, 0], [0, 0, 0, 3, 3, ..., i = 0, span = 4, j = 5, low = 3, high = 4, best = 2, k = 4`     |
| `high = min(j - 1, best_cut[i + 1][j])`  | `dp = [[0, 0, 3, 7, 10, 0], [0, 0, 0, 3, 6, 0], [0, 0, 0, 0, 2,..., best_cut = [[0, 1, 1, 1, 2, 0], [0, 0, 2, 2, 2, 0], [0, 0, 0, 3, 3, ..., i = 1, low = 2, best = 5, k = 2, value = 5`                     |
| `return`                                 | `returned = 16`                                                                                                                                                                                              |

### Complexity

- Time: O(m^2). Knuth's optimisation: the best cut for `[i, j]` lies between the best cuts for `[i, j - 1]` and `[i + 1, j]`, so each diagonal of the `m x m` table costs only O(m) in total.
- Space: O(m^2). The cost table and the best-cut table (`m` = number of cuts + 2).
