---
name: sheet-ship-within-days
title: 'Ship Packages Within D Days'
tags: [dsa-sheet, binary-search, binary-search-on-the-answer]
difficulty: Intermediate
---

## Statement

Packages with weights `weights[0], weights[1], ...` must be shipped **in this order**. Each day the ship carries a run of consecutive packages whose total weight is at most its **capacity**. Return the **smallest capacity** that ships all the packages within `days` days.

### Examples

**Example 1**

Input:

```python
ship_capacity([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5)
```

Output:

```text
15
```

Capacity 15 ships `1..5`, `6 7`, `8`, `9`, `10` in 5 days.

**Example 2**

Input:

```python
ship_capacity([3, 2, 2, 4, 1, 4], 3)
```

Output:

```text
6
```

Capacity 6 ships `3 2`, `2 4`, `1 4` in 3 days.

### Constraints

- `1 <= len(weights) <= 2 * 10**4`
- `1 <= days <= len(weights)`
- `1 <= weights[i] <= 10**4`
- Trying every capacity one by one is too slow for the large tests.

## Theory

The answer is a capacity, and a ship that can carry `c` can also carry any bigger `c`, so "shippable within `days`" is `False ... False True ... True`: **binary search on the answer**.

The capacity must be at least `max(weights)` (every package has to fit alone) and never needs to exceed `sum(weights)` (one day for everything). To test a capacity, simulate greedily: load packages until the next one would overflow, then start a new day. Count the days; the capacity works if the count is at most `days`. `O(n log S)`.

## Explanation

`lo = max(weights)`, `hi = sum(weights)`. `needed(mid)` starts at one day and counts a new day whenever adding the next weight would exceed `mid`. A working capacity keeps the lower half, otherwise `lo = mid + 1`.
