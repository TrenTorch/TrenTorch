---
name: sheet-top-k-frequent
title: 'Top K Frequent Values'
tags: [dsa-sheet, hashing, hashing-patterns]
difficulty: Intermediate
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

## Theory

Count with a `Counter`, then pick the best `k`. Sorting all the distinct values by `(-count, value)` costs `O(m log m)` for `m` distinct values, which is fine here. A **heap** can pick the top `k` faster when `k` is small: `heapq.nsmallest(k, items, key=...)` keeps only `k` candidates, `O(m log k)`.

**Bucket sort** is the `O(n)` way: a frequency can be at most `n`, so put each value into a list at index `count`, then read the buckets from the highest index down. It needs more code but no sorting at all.

The tuple key `(-count, value)` is the standard way to say "bigger count first, smaller value on ties".

## Explanation

`counts.items()` are `(value, count)` pairs. `heapq.nsmallest(k, counts, key=lambda v: (-counts[v], v))` returns the `k` values with the smallest keys, which are the most frequent (and smallest on ties), already in the right order.
