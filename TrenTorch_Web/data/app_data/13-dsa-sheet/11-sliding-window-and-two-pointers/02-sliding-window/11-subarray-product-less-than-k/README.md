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

**Explanation:** With nums=[10,5,2,6] and k=100 the algorithm expands right shrinks left when product>=100 and adds right-left+1 each step counting subarrays ending at right with product<100 totaling 8.

**Example 2**

Input:

```python
count_product_less([1, 2, 3], 0)
```

Output:

```text
0
```

**Explanation:** nums=[1,2,3] and k=0 means no product can be strictly less than zero since all numbers are positive so output is 0.

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

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line             | Variables                                    |
| --------------------------- | -------------------------------------------- |
| `product = 1`               | `product = 1`                                |
| `total = 0`                 | `left = 0, total = 0`                        |
| `total += right - left + 1` | `product = 10, total = 1, right = 0, x = 10` |
| `product *= x`              | `product = 50, right = 1, x = 5`             |
| `product *= x`              | `product = 100, total = 3, right = 2, x = 2` |
| `left += 1`                 | `product = 10, left = 1`                     |
| `product *= x`              | `product = 60, total = 5, right = 3, x = 6`  |
| `return`                    | `returned = 8`                               |

### Complexity

- Time: O(n), n is number of elements.
- Extra space: O(1), n = len(nums), q = k.
- The brute force takes O(n^2), n = len(nums), q = k.
