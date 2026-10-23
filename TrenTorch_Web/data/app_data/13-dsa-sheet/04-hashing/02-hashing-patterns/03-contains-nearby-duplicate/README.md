---
name: sheet-contains-nearby-duplicate
title: 'Nearby Duplicate'
tags: [dsa-sheet, hashing, hashing-patterns]
difficulty: Intermediate
---

## Statement

Return `True` if there are two **different positions** `i` and `j` with `nums[i] == nums[j]` and `abs(i - j) <= k`. Otherwise return `False`.

The starter code compares every pair. It is correct but too slow. Make it fast.

### Examples

**Example 1**

Input:

```python
contains_nearby_duplicate([1, 2, 3, 1], 3)
```

Output:

```text
True
```

The two `1`s are 3 positions apart.

**Example 2**

Input:

```python
contains_nearby_duplicate([1, 2, 3, 1, 2, 3], 2)
```

Output:

```text
False
```

Equal values are always 3 positions apart, more than 2.

### Constraints

- `0 <= len(nums) <= 2 * 10**5`
- `0 <= k <= 2 * 10**5`
- `-10**9 <= nums[i] <= 10**9`

## Theory

Comparing each value with its next `k` neighbours costs `O(n * k)`. Remember where each value was **last seen** in a dictionary.

When you reach position `i` with value `x`, the nearest earlier copy of `x` is at `last[x]`. If `i - last[x] <= k` you have found a close pair. Whether or not you found one, update `last[x] = i`: a later copy will be closest to the newest position, so older positions are never needed again.

Remembering only the **most recent** position is the trick: it is enough because the closest pair for any value always uses neighbouring occurrences.

## Explanation

`last` maps a value to the index where it last appeared. If the same value appeared at most `k` positions ago, return `True`. Always overwrite `last[x]` with the current index. Reaching the end means no close pair exists.
