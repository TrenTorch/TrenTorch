---
name: sheet-min-days-bouquets
title: 'Days to Make Bouquets'
tags: [dsa-sheet, binary-search, binary-search-on-the-answer]
difficulty: Intermediate
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

## Theory

Again **binary search on the answer**: the answer is a day, and once enough bouquets are possible on day `d`, they are possible on every later day (flowers do not un-bloom). So "possible by day `d`" goes `False ... False True ... True`.

Impossible is easy to spot first: you need `m * k` flowers, so if `m * k > len(bloom)` return `-1`.

To check a day `d`, sweep the flowers once, counting the current run of bloomed neighbours: a flower with `bloom[i] <= d` extends the run; when the run reaches `k`, count a bouquet and start a new run; an unbloomed flower resets the run. The day range is `min(bloom)` to `max(bloom)`. `O(n log M)`.

## Explanation

If `m * k` is more than the number of flowers, return `-1`. Otherwise search days between the earliest and latest bloom. `possible(day)` counts bouquets in one pass using the run length. A day that works keeps the lower half, a day that does not moves `lo` up.
