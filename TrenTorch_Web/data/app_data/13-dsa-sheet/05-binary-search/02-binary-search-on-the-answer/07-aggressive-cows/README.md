---
name: sheet-aggressive-cows
title: 'Place the Cows Far Apart'
tags: [dsa-sheet, binary-search, binary-search-on-the-answer]
difficulty: Advanced
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

## Theory

This one **maximises a minimum**, which is a classic sign of binary search on the answer. If you can place the cows with every pair at least `d` apart, you can also do it for any smaller `d`. So "possible with distance `d`" goes `True ... True False ... False`, and you want the last `True`.

Check a distance greedily: sort the stalls, put the first cow in the first stall, and keep putting the next cow in the first stall that is at least `d` farther than the last one. If you manage to place all the cows, `d` works. Greedy is optimal because pushing each cow as far left as possible leaves the most room.

The distance ranges from `1` to `max - min`. `O(n log M)` plus the sort.

## Explanation

Sort `stalls`. `place(d)` puts a cow in the first stall, then a cow in each next stall at least `d` after the previous cow, counting them. Search `d` upward: if `place(mid) >= cows` the distance works and `lo = mid`, otherwise `hi = mid - 1`. The `+ 1` in `mid = (lo + hi + 1) // 2` stops an endless loop when `lo` can move.
