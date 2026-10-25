---
name: sheet-array-leaders
title: 'Leaders in an Array'
tags: [dsa-sheet, arrays, array-basics]
difficulty: Beginner
---

## Statement

A **leader** is a value that is strictly greater than **every value to its right**. The last value is always a leader. Return the leaders in their original left-to-right order.

A simple solution compares each value with everything after it. It is correct but too slow for long lists. Make it fast.

### Examples

**Example 1**

Input:

```python
array_leaders([16, 17, 4, 3, 5, 2])
```

Output:

```text
[17, 5, 2]
```

`17`, `5` and `2` are each bigger than everything to their right.

**Example 2**

Input:

```python
array_leaders([5, 5, 5])
```

Output:

```text
[5]
```

Equal values do not count: only the last `5` is a leader.

### Constraints

- `0 <= len(nums) <= 3 * 10**5`
- `-10**9 <= nums[i] <= 10**9`

## Theory

Checking each value against everything to its right is `O(n²)`. Flip the direction: scan from the **right** and remember the largest value seen so far. A value is a leader exactly when it beats that running maximum.

Scanning from the end is a useful trick whenever the answer for a position depends on what comes _after_ it. The leaders are found in right-to-left order, so reverse the list at the end.

## Explanation

Walk `reversed(nums)`, keeping `best`. A value `x > best` (or the first value, when `best` is `None`) is a leader: append it and raise `best`. Reverse the collected list to restore the left-to-right order.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line            | Variables                  |
| -------------------------- | -------------------------- |
| `out = []`                 | `out = []`                 |
| `for x in reversed(nums):` | `best = None, x = 2`       |
| `best = x`                 | `out = [2], best = 2`      |
| `out.append(x)`            | `out = [2, 5], x = 5`      |
| `for x in reversed(nums):` | `best = 5, x = 4`          |
| `out.append(x)`            | `out = [2, 5, 17], x = 17` |
| `for x in reversed(nums):` | `best = 17, x = 16`        |
| `return`                   | `returned = [17, 5, 2]`    |

### Complexity

- Time: O(n) where n is the length of nums.
- Extra space: O(n) where n is the length of nums.
- The brute force takes O(n^2) where n is the length of nums.
