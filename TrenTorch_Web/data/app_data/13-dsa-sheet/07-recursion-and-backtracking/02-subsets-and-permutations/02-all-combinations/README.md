---
name: sheet-all-combinations
title: 'All Combinations of K Numbers'
tags: [dsa-sheet, recursion, subsets-and-permutations]
difficulty: Beginner
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

## Theory

Choose the numbers in increasing order, one at a time. `go(start, current)` needs `k - len(current)` more numbers, all from `start..n`. Try each `j` from `start`, add it, recurse from `j + 1`, remove it.

**Prune** with a counting argument: if you still need `r` numbers, the last useful starting point is `n - r + 1`, because later starts leave too few numbers to finish. Stopping the loop there avoids many dead branches.

There are `C(n, k)` answers, so the output itself is large. The standard library has `itertools.combinations`, but writing the recursion yourself is the exercise.

## Explanation

`need = k - len(current)` is how many numbers are still missing. The loop runs `j` from `start` to `n - need + 1`: beyond that there are not enough numbers left. When `need` is `0`, record a copy.
