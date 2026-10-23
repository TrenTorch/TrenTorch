---
name: sheet-all-subset-sums
title: 'All Subset Sums'
tags: [dsa-sheet, recursion, recursive-thinking]
difficulty: Beginner
---

## Statement

Return the **sum of every subset** of `nums` (including the empty subset, whose sum is `0`), as one sorted list with repeats kept. A list of `n` values has `2^n` subsets.

### Examples

**Example 1**

Input:

```python
all_subset_sums([1, 2])
```

Output:

```text
[0, 1, 2, 3]
```

**Example 2**

Input:

```python
all_subset_sums([])
```

Output:

```text
[0]
```

### Constraints

- `0 <= len(nums) <= 16`
- `-1000 <= nums[i] <= 1000`

## Theory

Each value is either **in** a subset or **out**. If you already know all the sums of the first `i` values, adding value `x` doubles the list: every old sum stays (x is out), and every old sum plus `x` is new (x is in).

So start with `[0]` and for each value do `sums = sums + [s + x for s in sums]`. There is no recursion and no backtracking, only the doubling idea behind it. The final list has `2^n` sums, so the work is `O(2^n)`.

Sorting the result puts it in the required order. Recursion expresses the same thing as "sum without `x`" and "sum with `x`".

## Explanation

`sums` starts as `[0]` (the empty subset). For each value, the sums that include it are the old sums plus the value; append them to the old ones. Sort at the end.
