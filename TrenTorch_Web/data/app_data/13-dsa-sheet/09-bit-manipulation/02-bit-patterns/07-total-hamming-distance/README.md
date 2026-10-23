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

**Example 2**

Input:

```python
total_hamming_distance([4, 14, 4])
```

Output:

```text
4
```

### Constraints

- `1 <= len(nums) <= 50000`
- `0 <= nums[i] < 2**30`

## Theory

Instead of pairs, think **per bit position**. At position `i`, suppose `k` of the `n` numbers have a `1` and `n - k` have a `0`. A pair differs at this position exactly when one number is from each group: `k * (n - k)` pairs.

So the answer is `sum over positions of k * (n - k)`. That is 30 positions, each a pass over the list: `O(30 n)` instead of `O(n²)`.

This **count per bit** idea turns many pair problems into counting problems.

## Explanation

For each bit, `ones` counts the numbers that have it set; each of them differs there from each of the `n - ones` numbers that do not.
