---
name: sheet-subarray-product-less-than-k
title: 'Subarrays With Product Less Than K'
tags: [dsa-sheet, sliding-window, sliding-window]
difficulty: Intermediate
theory: counting-windows-product-below-k
---

## Statement

`nums` contains positive whole numbers. Count the contiguous subarrays whose **product is strictly less than `k`**.

For `nums = [10, 5, 2, 6]` and `k = 100` the answer is `8`.

The starter code multiplies out every subarray. It is correct but too slow when many subarrays qualify.

### Examples

**Example 1**

Input:

```python
count_product_less([10, 5, 2, 6], 100)
```

Output:

```text
8
```

**Example 2**

Input:

```python
count_product_less([1, 2, 3], 0)
```

Output:

```text
0
```

### Constraints

- `0 <= len(nums) <= 200000`
- `1 <= nums[i] <= 1000`
- `0 <= k <= 10**9`

## Explanation

The check `left <= right` stops the loop when `k <= 1` and even a single element is too big; the window is then empty and adds 0.

### Complexity

- Time: O(n). Each index enters and leaves the window once (values are positive).
- Space: O(1). A few numbers.
