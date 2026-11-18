---
name: sheet-ship-within-days
title: 'Ship Packages Within D Days'
tags: [dsa-sheet, binary-search, binary-search-on-the-answer]
difficulty: Intermediate
theory: cutting-a-row-into-days
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

## Explanation

`lo = max(weights)`, `hi = sum(weights)`. `needed(mid)` starts at one day and counts a new day whenever adding the next weight would exceed `mid`. A working capacity keeps the lower half, otherwise `lo = mid + 1`.

### Complexity

- Time: O(n log W). Binary search over capacities up to the total weight `W` costs `log W` probes, and each probe scans `n` packages.
- Space: O(1). A few counters.
