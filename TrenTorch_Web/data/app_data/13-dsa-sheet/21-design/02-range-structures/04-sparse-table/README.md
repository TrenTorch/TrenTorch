---
name: sheet-sparse-table
title: 'Sparse Table (Static Range Minimum)'
tags: [dsa-sheet, design, range-structures]
difficulty: Advanced
---

## Statement

`nums` never changes. Each query `[l, r]` asks for the **smallest value in `nums[l..r]`** (both ends included). Return the answers in order.

For `nums = [5, 2, 8, 1, 9]` and `queries = [[0, 4], [1, 2], [2, 2]]` the answer is `[1, 2, 8]`.

The starter code scans the range for each query. It is correct but too slow for many queries.

### Examples

**Example 1**

Input:

```python
range_minimums([5, 2, 8, 1, 9], [[0, 4], [1, 2], [2, 2]])
```

Output:

```text
[1, 2, 8]
```

**Example 2**

Input:

```python
range_minimums([3], [[0, 0]])
```

Output:

```text
[3]
```

### Constraints

- `1 <= len(nums) <= 65536`
- `0 <= len(queries) <= 100000`
- `0 <= l <= r < len(nums)`
- `-10**9 <= nums[i] <= 10**9`

## Theory

In a **design** question you build a small data structure and run a list of operations on it. The operations are given as text, one per string, and you return the answers of the operations that produce one. Think about which operations must be fast and choose the data structure for them.

When the array never changes, you can precompute answers for **blocks whose length is a power of two**. Let `table[k][i]` be the minimum of `nums[i .. i + 2^k - 1]`. Level 0 is the array itself, and each higher level combines two blocks of the level below: `table[k][i] = min(table[k-1][i], table[k-1][i + 2^(k-1)])`. This has `log n` levels: `O(n log n)` memory and time.

A query `[l, r]` uses the largest `k` with `2^k <= r - l + 1`. Two blocks of length `2^k`, one starting at `l` and one ending at `r`, **overlap** but together cover the range exactly, and for a minimum the overlap does not matter: `min(table[k][l], table[k][r - 2^k + 1])`. Each query is `O(1)`.

## Explanation

`(r - l + 1).bit_length() - 1` is `floor(log2(length))`. The two table entries cover the range from both ends.
