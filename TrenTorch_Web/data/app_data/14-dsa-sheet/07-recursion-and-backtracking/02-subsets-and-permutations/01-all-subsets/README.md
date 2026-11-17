---
name: sheet-all-subsets
title: 'All Subsets'
tags: [dsa-sheet, recursion, subsets-and-permutations]
difficulty: Beginner
theory: subsets-in-dictionary-order
---

## Statement

`nums` holds **different** values. Return **every subset** (including the empty one and the whole list). Write each subset in increasing order, and list the subsets in **dictionary order** (compare the first value, then the second, and so on; a shorter list that is the start of a longer one comes first).

For `[1, 2, 3]` that is `[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]`.

### Examples

**Example 1**

Input:

```python
all_subsets([1, 2, 3])
```

Output:

```text
[[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]]
```

**Example 2**

Input:

```python
all_subsets([])
```

Output:

```text
[[]]
```

### Constraints

- `0 <= len(nums) <= 14`
- All values are different.
- `-100 <= nums[i] <= 100`

## Explanation

`go(i, cur)` first records a copy of `cur` (every partial choice is itself a subset), then tries each value from index `i` onwards: add it, recurse on the rest, remove it. Copy `cur` with `list(cur)` when recording, because `cur` keeps changing.

### Complexity

- Time: O(n * 2^n). There are `2^n` subsets and copying each into the output costs up to `n`.
- Space: O(n * 2^n). The output; the recursion adds only `O(n)`.
