---
name: sheet-partition-equal-subset-sum
title: 'Partition Equal Subset Sum'
tags: [dsa-sheet, dynamic-programming, sequences-and-counting]
difficulty: Intermediate
theory: subset-sum-and-its-cousins
---

## Statement

Return `True` if the numbers in `nums` can be split into **two groups with the same sum**.

For `[1, 5, 11, 5]` the answer is `True` (`11` and `1 + 5 + 5`); for `[1, 2, 3, 5]` it is `False`.

The starter code tries to include or skip every number. It is correct but too slow on inputs without an answer.

### Examples

**Example 1**

Input:

```python
can_partition([1, 5, 11, 5])
```

Output:

```text
True
```

**Example 2**

Input:

```python
can_partition([1, 2, 3, 5])
```

Output:

```text
False
```

### Constraints

- `0 <= len(nums) <= 200`
- `1 <= nums[i] <= 100`

## Explanation

Bit `s` of `bits` means "a subset with sum `s` exists". The shift by `x` adds `x` to every reachable sum at once.

### Complexity

- Time: O(n * S / w). `S` is the total sum and `w` the machine word size: each number shifts and ORs one big integer used as a bit set of reachable sums.
- Space: O(S / w). The bit set.
