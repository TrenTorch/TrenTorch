---
name: sheet-subsets-with-duplicates
title: 'Subsets With Repeated Values'
tags: [dsa-sheet, recursion, subsets-and-permutations]
difficulty: Intermediate
theory: repeated-values-in-subsets
---

## Statement

`nums` may contain **repeated values**. Return every **different subset** (two subsets are the same if they hold the same values with the same counts). Write each subset in increasing order and list the subsets in dictionary order.

For `[1, 2, 2]`: `[], [1], [1, 2], [1, 2, 2], [2], [2, 2]`.

### Examples

**Example 1**

Input:

```python
subsets_with_duplicates([1, 2, 2])
```

Output:

```text
[[], [1], [1, 2], [1, 2, 2], [2], [2, 2]]
```

**Example 2**

Input:

```python
subsets_with_duplicates([0])
```

Output:

```text
[[], [0]]
```

### Constraints

- `0 <= len(nums) <= 14`
- `-100 <= nums[i] <= 100`

## Explanation

The loop starts at `start`. A value equal to the one before it **within the same loop** is skipped because that choice would build exactly the same subsets as the earlier one. Values further down the recursion start a new loop, so a second equal value can still be taken after the first.

### Complexity

- Time: O(n * 2^n). At most `2^n` subsets, each copied once; skipping equal neighbours at the same depth stops duplicates before they are built.
- Space: O(n * 2^n). The output; the recursion adds only `O(n)`.
