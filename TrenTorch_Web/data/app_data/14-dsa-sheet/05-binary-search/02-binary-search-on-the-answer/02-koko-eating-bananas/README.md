---
name: sheet-koko-eating-bananas
title: 'Eating Speed'
tags: [dsa-sheet, binary-search, binary-search-on-the-answer]
difficulty: Intermediate
theory: the-slowest-speed-that-works
---

## Statement

There are piles of bananas, `piles[i]` in pile `i`. You eat at a speed of `k` bananas per hour. Each hour you pick **one pile** and eat up to `k` bananas from it; if the pile has fewer than `k` left you finish it and waste the rest of that hour.

Return the **smallest whole `k`** that lets you finish every pile within `hours` hours.

### Examples

**Example 1**

Input:

```python
min_eating_speed([3, 6, 7, 11], 8)
```

Output:

```text
4
```

Speed 4 takes 1 + 2 + 2 + 3 = 8 hours.

**Example 2**

Input:

```python
min_eating_speed([30, 11, 23, 4, 20], 5)
```

Output:

```text
30
```

With 5 hours for 5 piles you must finish a pile every hour, so the speed is the biggest pile: 30.

### Constraints

- `1 <= len(piles) <= 2 * 10**4`
- `len(piles) <= hours <= 10**9`
- `1 <= piles[i] <= 10**9`
- Trying every speed one by one is too slow for the large tests.

## Explanation

`lo = 1`, `hi = max(piles)`. For each `mid`, `needed = sum(-(-p // mid) for p in piles)`. If `needed <= hours` the speed works, so try slower: `hi = mid`. Otherwise it is too slow: `lo = mid + 1`. The loop ends at the smallest working speed.

### Complexity

- Time: O(n log M). Binary search over speeds `1..M` (`M` = largest pile) costs `log M` probes, and each probe sums `n` piles.
- Space: O(1). Two bounds and a running sum.
