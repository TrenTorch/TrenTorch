---
name: sheet-contains-nearby-duplicate
title: 'Nearby Duplicate'
tags: [dsa-sheet, hashing, hashing-patterns]
difficulty: Intermediate
theory: remembering-the-last-place-we-saw-it
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

## Explanation

The set holds the values of the last `k` positions. Before adding `x`, check whether it is already in the set: a hit means the same value appeared at most `k` positions ago, so return `True`. After adding `x`, drop the value that just fell out of range, `nums[i - k]`. With `k = 0` the window is always empty, so the answer is `False`.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                | Variables                       |
| ------------------------------ | ------------------------------- |
| `window = set()`               | `window = set()`                |
| `for i, x in enumerate(nums):` | `i = 0, x = 1`                  |
| `window.add(x)`                | `window = {1}`                  |
| `for i, x in enumerate(nums):` | `i = 1, x = 2`                  |
| `for i, x in enumerate(nums):` | `window = {1, 2}, i = 2, x = 3` |
| `window.add(x)`                | `window = {1, 2, 3}`            |
| `for i, x in enumerate(nums):` | `i = 3, x = 1`                  |
| `return`                       | `returned = True`               |

### Complexity

- Time: O(n). One pass; set lookups, inserts and removals are O(1) on average.
- Space: O(min(n, k)). The set holds only the last `k` values.
