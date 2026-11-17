---
name: sheet-aggressive-cows
title: 'Place the Cows Far Apart'
tags: [dsa-sheet, binary-search, binary-search-on-the-answer]
difficulty: Advanced
theory: cows-in-stalls
---

## Statement

Stalls stand at the positions in `stalls` (not sorted). You must place `cows` cows in different stalls so that the **smallest distance between any two cows is as large as possible**. Return that largest smallest distance.

### Examples

**Example 1**

Input:

```python
aggressive_cows([1, 2, 4, 8, 9], 3)
```

Output:

```text
3
```

Cows at 1, 4 and 8 give a smallest distance of 3.

**Example 2**

Input:

```python
aggressive_cows([10, 1, 2, 7, 5], 3)
```

Output:

```text
4
```

Cows at 1, 5 and 10 give a smallest distance of 4.

### Constraints

- `2 <= cows <= len(stalls) <= 2 * 10**4`
- `0 <= stalls[i] <= 10**9`, and the positions are different
- Trying every distance one by one is too slow for the large tests.

## Explanation

Sort `stalls`. `place(d)` puts a cow in the first stall, then a cow in each next stall at least `d` after the previous cow, counting them. Search `d` upward: if `place(mid) >= cows` the distance works and `lo = mid`, otherwise `hi = mid - 1`. The `+ 1` in `mid = (lo + hi + 1) // 2` stops an endless loop when `lo` can move.

### Complexity

- Time: O(n log n + n log D). Sort the stalls, then binary search the distance (`D` = last stall minus first) with one `O(n)` scan per probe.
- Space: O(n). The sorted copy.
