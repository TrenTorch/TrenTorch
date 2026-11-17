---
name: sheet-top-k-frequent
title: 'Top K Frequent Values'
tags: [dsa-sheet, hashing, hashing-patterns]
difficulty: Intermediate
theory: buckets-for-counts
---

## Statement

Return the `k` **most frequent** values of `nums`, from the most frequent to the least. If two values have the same frequency, the **smaller value** comes first. If there are fewer than `k` different values, return all of them.

### Examples

**Example 1**

Input:

```python
top_k_frequent([1, 1, 1, 2, 2, 3], 2)
```

Output:

```text
[1, 2]
```

`1` appears 3 times, `2` appears 2 times.

**Example 2**

Input:

```python
top_k_frequent([4, 5, 5, 4], 1)
```

Output:

```text
[4]
```

`4` and `5` tie, so the smaller value wins.

### Constraints

- `0 <= len(nums) <= 3 * 10**5`
- `0 <= k <= 3 * 10**5`
- `-10**9 <= nums[i] <= 10**9`

## Explanation

Count the values, then order them by `(-count, value)`: the first `k` in that order are the answer. Instead of sorting all distinct values, use quickselect: pick a random pivot pair, split the pairs into smaller and larger (the pairs are all different because the values are), and keep only the side that contains the `k`-th pair. Then sort just the `k` chosen pairs.

`heapq.nsmallest(k, counts, key=...)` does the same job with a heap, in `O(n + d log k)`.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                                                       | Variables                                      |
| --------------------------------------------------------------------- | ---------------------------------------------- |
| `pairs = [(-count, value) for value, count in Counter(nums).items()]` | `pairs = [(-3, 1), (-2, 2), (-1, 3)]`          |
| `chosen = []`                                                         | `chosen = []`                                  |
| `need = k`                                                            | `pool = [(-3, 1), (-2, 2), (-1, 3)], need = 2` |
| `pivot = random.choice(pool)`                                         | `pivot = (-2, 2)`                              |
| `chosen += less`                                                      | `chosen = [(-3, 1)], less = [(-3, 1)]`         |
| `chosen.append(pivot)`                                                | `chosen = [(-3, 1), (-2, 2)]`                  |
| `pairs = chosen`                                                      | `pairs = [(-3, 1), (-2, 2)], need = 0`         |
| `return`                                                              | `returned = [1, 2]`                            |

### Complexity

- Time: O(n + k log k) expected. Counting is O(n); quickselect on the `d` distinct values is expected O(d); only the chosen `k` are sorted.
- Space: O(d). The counter and the list of `(-count, value)` pairs.
