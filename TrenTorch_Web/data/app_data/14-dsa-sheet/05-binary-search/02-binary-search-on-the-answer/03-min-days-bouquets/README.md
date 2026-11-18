---
name: sheet-min-days-bouquets
title: 'Days to Make Bouquets'
tags: [dsa-sheet, binary-search, binary-search-on-the-answer]
difficulty: Intermediate
theory: same-pattern-new-stories
---

## Statement

`bloom[i]` is the day on which flower `i` blooms. A bouquet uses `k` **neighbouring** flowers (positions next to each other) that have all bloomed, and each flower can be used in only one bouquet. Return the **earliest day** by which you can make `m` bouquets, or `-1` if it is impossible.

### Examples

**Example 1**

Input:

```python
min_days_bouquets([1, 10, 3, 10, 2], 3, 1)
```

Output:

```text
3
```

On day 3 flowers 0, 2 and 4 have bloomed: 3 bouquets of 1.

**Example 2**

Input:

```python
min_days_bouquets([7, 7, 7, 7, 12, 7, 7], 2, 3)
```

Output:

```text
12
```

On day 12 everything has bloomed: `[7,7,7]` and `[7,7,7]` around the `12`.

### Constraints

- `1 <= len(bloom) <= 2 * 10**4`
- `1 <= bloom[i] <= 10**9`
- `1 <= m, k <= 2 * 10**4`
- Trying every day one by one is too slow for the large tests.

## Explanation

If `m * k` is more than the number of flowers, return `-1`. Otherwise search days between the earliest and latest bloom. `possible(day)` counts bouquets in one pass using the run length. A day that works keeps the lower half, a day that does not moves `lo` up.

### Complexity

- Time: O(n log D). Binary search over the days between the first and the last bloom (`D` = latest bloom day) costs `log D` probes, and each probe scans `n` flowers.
- Space: O(1). A few counters.
