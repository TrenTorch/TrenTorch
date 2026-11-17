---
name: sheet-sort-records
title: 'Leaderboard Order'
tags: [dsa-sheet, basics, python-toolbox]
difficulty: Beginner
theory: sorting-with-a-key
---

## Statement

Each record is `[name, score]`. Return the list of names ordered by score from highest to lowest. When two records have the same score, the name that comes first alphabetically goes first.

A name can appear in more than one record; keep every record.

### Examples

**Example 1**

Input:

```python
sort_records([['bo', 5], ['al', 9], ['cy', 5]])
```

Output:

```text
['al', 'bo', 'cy']
```

`al` has the top score. `bo` and `cy` tie on 5, so `bo` comes first.

**Example 2**

Input:

```python
sort_records([['zed', 1]])
```

Output:

```text
['zed']
```

### Constraints

- `0 <= len(records) <= 2 * 10**5`
- `name` is a lower-case string, `0 <= score <= 10**9`

## Explanation

The key `(-score, name)` sorts by negative score (so higher scores come first), and uses the name only when the scores are equal.

Then pull out the names. Sorting once with a tuple key is faster and clearer than sorting twice.

### Complexity

- Time: O(n log n). One comparison sort (Timsort) with a key; no comparison sort can do better.
- Space: O(n). The sorted copy and the key list.
