---
name: sheet-count-frequencies
title: 'Frequency Queries'
tags: [dsa-sheet, hashing, counting-with-dictionaries]
difficulty: Beginner
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

## Theory

Counting one value in a list costs `O(n)`. Doing it for `q` queries costs `O(n * q)`.

A **hash table** removes the repeated work. In Python a `dict` stores a value under a _key_, and finds it in `O(1)` on average by computing the key's **hash**: a number that tells where to look, instead of scanning everything. `collections.Counter` is a dictionary built for counting: `Counter(nums)` counts every value in one pass, and `counts[v]` answers a query instantly (a missing key gives `0`).

The pattern is: **pay `O(n)` once to build a table, then answer each query in `O(1)`**. It appears in almost every hashing problem.

## Explanation

Build `counts = Counter(nums)` once. Each query is then `counts[q]`, and a value that never appears gives `0` without raising an error. Total time is `O(n + q)`.
