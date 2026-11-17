---
name: sheet-count-frequencies
title: 'Frequency Queries'
tags: [dsa-sheet, hashing, counting-with-dictionaries]
difficulty: Beginner
theory: counting-how-often-things-appear
---

## Statement

For every value in `queries`, return how many times it appears in `nums`. Return the answers in the same order as the queries.

The starter code counts again from scratch for every query. It is correct but too slow when both lists are long. Make it fast.

### Examples

**Example 1**

Input:

```python
count_frequencies([1, 2, 2, 3, 3, 3], [3, 2, 5])
```

Output:

```text
[3, 2, 0]
```

**Example 2**

Input:

```python
count_frequencies([], [1])
```

Output:

```text
[0]
```

### Constraints

- `0 <= len(nums), len(queries) <= 2 * 10**5`
- `-10**9 <= value <= 10**9`

## Explanation

Build `counts = Counter(nums)` once. Each query is then `counts[q]`, and a value that never appears gives `0` without raising an error. Total time is `O(n + q)`.

### Complexity

- Time: O(n + q). One pass to count `n` values and one lookup for each of the `q` queries.
- Space: O(n). The counter may hold all `n` distinct values (the answer list of size `q` is output).
