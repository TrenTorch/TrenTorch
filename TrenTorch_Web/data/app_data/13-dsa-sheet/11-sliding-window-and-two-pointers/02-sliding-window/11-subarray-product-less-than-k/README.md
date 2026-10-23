---
name: sheet-subarray-product-less-than-k
title: 'Subarrays With Product Less Than K'
tags: [dsa-sheet, sliding-window, sliding-window]
difficulty: Intermediate
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

## Theory

A **sliding window** is a range `[left, right]` of the data that grows on the right and shrinks on the left. Because each end only moves forward, the whole pass is `O(n)`, while the window always describes one candidate subarray or substring.

Because the numbers are **at least 1**, extending a subarray never lowers its product, so a window can be shrunk greedily. Keep the product of the window. Expand `right` (multiply). While the product is `>= k` (and the window is not empty), shrink from the left (divide).

For each `right`, **all** subarrays that end at `right` and start between `left` and `right` have a product below `k` (they are sub-windows, so their products are smaller): that is `right - left + 1` new subarrays. Sum them. `O(n)`.

## Explanation

The check `left <= right` stops the loop when `k <= 1` and even a single element is too big; the window is then empty and adds 0.
