---
name: sheet-burst-balloons
title: 'Burst Balloons'
tags: [dsa-sheet, dynamic-programming, intervals-and-states]
difficulty: Mastery
theory: burst-balloons-and-cutting-a-stick
---

## Statement

There are balloons with numbers `nums[i]`. Bursting balloon `i` gives `nums[i - 1] * nums[i] * nums[i + 1]` coins, where `i - 1` and `i + 1` are the **neighbours that are still there** (a missing neighbour counts as a balloon with number 1). Burst all balloons in the best order and return the **maximum coins**.

For `[3, 1, 5, 8]` the answer is `167`.

The starter code tries every order. It is correct but too slow for more than a few balloons.

### Examples

**Example 1**

Input:

```python
max_coins([3, 1, 5, 8])
```

Output:

```text
167
```

**Example 2**

Input:

```python
max_coins([1, 5])
```

Output:

```text
10
```

### Constraints

- `0 <= len(nums) <= 120`
- `0 <= nums[i] <= 100`

## Explanation

`dp[i][j]` is filled for increasing `j - i`. `k` runs over the balloons between the borders.

### Complexity

- Time: O(n^3). The table has `n^2` cells, each trying up to `n` last balloons.
- Space: O(n^2). The table.
