---
name: sheet-all-subsets
title: 'All Subsets'
tags: [dsa-sheet, recursion, subsets-and-permutations]
difficulty: Beginner
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

## Theory

Recursion is a function that calls itself on a smaller version of the same problem. Every recursive function needs a **base case** that stops and a **step** that moves toward it.

Subsets are a natural fit. Sort the values. A subset is built by deciding, one value at a time, what to include. The recursive function `go(start, current)` records `current` as a subset, then for each later value `j >= start` it **adds** `a[j]`, calls `go(j + 1, current)` to extend further, and then **removes** `a[j]` again (this undo step is **backtracking**). The result is produced in dictionary order for free.

There are `2^n` subsets, so any solution takes at least that long. That is why `n` is small.

## Explanation

`go(i, cur)` first records a copy of `cur` (every partial choice is itself a subset), then tries each value from index `i` onwards: add it, recurse on the rest, remove it. Copy `cur` with `list(cur)` when recording, because `cur` keeps changing.
