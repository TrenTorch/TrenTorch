---
name: sheet-pivot-index
title: 'Balance Point'
tags: [dsa-sheet, arrays, array-basics]
difficulty: Beginner
theory: left-sum-equals-right-sum
---

## Statement

Return the **leftmost index** `i` where the sum of the values to its left equals the sum of the values to its right (the value at `i` itself is not counted). An empty side has sum `0`. If no index works, return `-1`.

A simple solution adds up both sides for every index. It is correct but too slow for long lists. Make it fast.

### Examples

**Example 1**

Input:

```python
pivot_index([1, 7, 3, 6, 5, 6])
```

Output:

```text
3
```

At index 3 the left sum is 1+7+3 = 11 and the right sum is 5+6 = 11.

**Example 2**

Input:

```python
pivot_index([1, 2, 3])
```

Output:

```text
-1
```

No index balances.

### Constraints

- `0 <= len(nums) <= 2 * 10**5`
- `-10**4 <= nums[i] <= 10**4`

## Explanation

`left` starts at `0` and grows by `nums[i]` after each index is checked. The right sum is derived from the total, so no inner loop is needed. Negative values do not matter because only sums are compared.

### Complexity

- Time: O(n). One `sum` pass and one pass that keeps the left sum.
- Space: O(1). Two integers.
