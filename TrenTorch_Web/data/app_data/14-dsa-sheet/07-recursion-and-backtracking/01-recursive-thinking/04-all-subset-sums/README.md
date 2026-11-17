---
name: sheet-all-subset-sums
title: 'All Subset Sums'
tags: [dsa-sheet, recursion, recursive-thinking]
difficulty: Beginner
theory: take-it-or-leave-it
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

## Explanation

Start with `[0]`, the sum of the empty subset. For each number `x`, every existing sum can be taken with or without `x`, so the new list is the old list plus the old list shifted by `x`. Both halves are already sorted, so sorting their concatenation is a single linear merge (Timsort finds the two sorted runs), and the list stays sorted without a final sort.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                               | Variables                 |
| --------------------------------------------- | ------------------------- |
| `sums = [0]`                                  | `sums = [0]`              |
| `for x in nums:`                              | `x = 1`                   |
| `sums = sorted(sums + [s + x for s in sums])` | `sums = [0, 1]`           |
| `for x in nums:`                              | `x = 2`                   |
| `sums = sorted(sums + [s + x for s in sums])` | `sums = [0, 1, 2, 3]`     |
| `return`                                      | `returned = [0, 1, 2, 3]` |

### Complexity

- Time: O(2^n). Adding one more number doubles the sorted list; the shifted copy is already sorted, so merging the two sorted halves is linear, and the sizes add up to `2^(n+1)`.
- Space: O(2^n). The list of sums is the output.
