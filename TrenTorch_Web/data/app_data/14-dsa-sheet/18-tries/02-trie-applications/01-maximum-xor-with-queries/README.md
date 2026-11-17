---
name: sheet-maximum-xor-with-queries
title: 'Maximum XOR With Each Query'
tags: [dsa-sheet, tries, trie-applications]
difficulty: Advanced
theory: greedy-from-the-top-bit
---

## Statement

For each `x` in `queries`, return the **maximum of `x ^ n`** over all numbers `n` in `nums` (`^` is xor). `nums` is not empty.

For `nums = [0, 1, 2, 3, 4]` and `queries = [3, 5]` the answer is `[7, 7]`.

The starter code tries every number for every query. It is correct but too slow for many numbers and queries.

### Examples

**Example 1**

Input:

```python
max_xor_queries([0, 1, 2, 3, 4], [3, 5])
```

Output:

```text
[7, 7]
```

**Example 2**

Input:

```python
max_xor_queries([7], [7, 0])
```

Output:

```text
[0, 7]
```

### Constraints

- `1 <= len(nums) <= 15000`
- `0 <= len(queries) <= 15000`
- `0 <= nums[i], x < 2**30`

## Explanation

`want = 1 - bit` is the opposite bit. If that child exists, the xor gets a 1 at this position.

### Complexity

- Time: O(30 * (n + q)). A binary trie of the numbers is built with 30 steps per number; each query walks 30 levels, always preferring the opposite bit.
- Space: O(30 * n). The trie.
