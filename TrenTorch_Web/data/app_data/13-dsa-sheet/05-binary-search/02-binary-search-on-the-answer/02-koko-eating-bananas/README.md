---
name: sheet-koko-eating-bananas
title: 'Eating Speed'
tags: [dsa-sheet, binary-search, binary-search-on-the-answer]
difficulty: Intermediate
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

## Theory

This is **binary search on the answer**. A speed `k` either works (all piles done within `hours`) or not, and if `k` works then any faster speed also works. So the speeds that work form a block `False, False, ..., True, True, ...`. The answer is the first `True`.

The speed is between `1` and `max(piles)` (faster than the biggest pile never helps). For a guess `k`, the time needed is the sum over piles of `ceil(pile / k)`. In Python `-(-pile // k)` is a ceiling division with integers (no floats).

Check the guess in `O(n)`, and there are about `log₂ (max pile)` guesses: `O(n log M)` in total, instead of `O(n * M)` for trying every speed.

## Explanation

`lo = 1`, `hi = max(piles)`. For each `mid`, `needed = sum(-(-p // mid) for p in piles)`. If `needed <= hours` the speed works, so try slower: `hi = mid`. Otherwise it is too slow: `lo = mid + 1`. The loop ends at the smallest working speed.
