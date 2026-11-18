---
name: sheet-house-robber
title: 'House Robber'
tags: [dsa-sheet, dynamic-programming, sequences-and-counting]
difficulty: Beginner
theory: house-robber
---

## Statement

`nums[i]` is the money in house `i`. You may rob any houses, but **never two neighbouring houses**. Return the **largest total** you can take.

For `[2, 7, 9, 3, 1]` the answer is `12` (rob 2, 9 and 1).

The starter code tries both choices for every house. It is correct but too slow for many houses.

### Examples

**Example 1**

Input:

```python
rob([1, 2, 3, 1])
```

Output:

```text
4
```

**Example 2**

Input:

```python
rob([2, 7, 9, 3, 1])
```

Output:

```text
12
```

### Constraints

- `0 <= len(nums) <= 1000000`
- `0 <= nums[i] <= 10000`

## Explanation

`skip` is `best(i - 1)` and `take` is `best(i - 2)`; each round computes the new best and shifts.

### Complexity

- Time: O(n). One pass keeping the best total with and without the previous house.
- Space: O(1). Two numbers.
