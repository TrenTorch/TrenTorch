---
name: sheet-total-hamming-distance
title: 'Total Hamming Distance'
tags: [dsa-sheet, bit-manipulation, bit-patterns]
difficulty: Advanced
---

## Statement

The **Hamming distance** of two numbers is the number of bit positions where they differ. Return the **sum of the Hamming distances over all pairs** `(i, j)` with `i < j`.

For `[4, 14, 2]` (binary `0100`, `1110`, `0010`) the answer is `6`.

The starter code checks every pair. It is correct but too slow for long lists.

### Examples

**Example 1**

Input:

```python
total_hamming_distance([4, 14, 2])
```

Output:

```text
6
```

**Explanation:** For [4, 14, 2], bit positions differ for pairs (4,14), (4,2), and (14,2) at 2, 3, and 1 positions respectively, totaling 6.

**Example 2**

Input:

```python
total_hamming_distance([4, 14, 4])
```

Output:

```text
4
```

**Explanation:** For [4, 14, 4], pairs (4,14), (4,4), and (14,4) produce distances 2, 0, and 2, summing to 4.

### Constraints

- `1 <= len(nums) <= 50000`
- `0 <= nums[i] < 2**30`

## Theory

Instead of pairs, think **per bit position**. At position `i`, suppose `k` of the `n` numbers have a `1` and `n - k` have a `0`. A pair differs at this position exactly when one number is from each group: `k * (n - k)` pairs.

So the answer is `sum over positions of k * (n - k)`. That is 30 positions, each a pass over the list: `O(30 n)` instead of `O(n²)`.

This **count per bit** idea turns many pair problems into counting problems.

## Explanation

For each bit, `ones` counts the numbers that have it set; each of them differs there from each of the `n - ones` numbers that do not.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line              | Variables                    |
| ---------------------------- | ---------------------------- |
| `n = len(nums)`              | `n = 3`                      |
| `total += ones * (n - ones)` | `total = 2, i = 1, ones = 2` |
| `total += ones * (n - ones)` | `total = 6, i = 3, ones = 1` |
| `for i in range(30):`        | `i = 8, ones = 0`            |
| `for i in range(30):`        | `i = 13`                     |
| `for i in range(30):`        | `i = 19`                     |
| `for i in range(30):`        | `i = 24`                     |
| `return`                     | `returned = 6`               |

### Complexity

- Time: O(n) where n is length of nums.
- Extra space: O(1), using only constant extra space for variables.
- The brute force takes O(n^2) where n is length of nums.
