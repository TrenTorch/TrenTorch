---
name: sheet-all-combinations
title: 'All Combinations of K Numbers'
tags: [dsa-sheet, recursion, subsets-and-permutations]
difficulty: Beginner
theory: combinations-and-cutting-dead-branches
---

## Statement

Return every way to **choose `k` numbers from `1, 2, ..., n`**, each written in increasing order, listed in dictionary order. For `n = 4` and `k = 2`: `[1,2], [1,3], [1,4], [2,3], [2,4], [3,4]`.

### Examples

**Example 1**

Input:

```python
all_combinations(4, 2)
```

Output:

```text
[[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]
```

**Example 2**

Input:

```python
all_combinations(1, 1)
```

Output:

```text
[[1]]
```

### Constraints

- `1 <= n <= 20`
- `0 <= k <= n`
- The answer has at most `C(n, k)` lists; the tests keep it under 200,000.

## Explanation

`need = k - len(current)` is how many numbers are still missing. The loop runs `j` from `start` to `n - need + 1`: beyond that there are not enough numbers left. When `need` is `0`, record a copy.

### Complexity

- Time: O(k * C(n, k)). There are `C(n, k)` combinations; each is copied once, and the loop bound stops branches that cannot reach size `k`.
- Space: O(k * C(n, k)). The output; the recursion adds only `O(k)`.
