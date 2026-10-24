---
name: sheet-count-subset-sums
title: 'Count Subsets With Sum'
tags: [dsa-sheet, basics, python-toolbox]
difficulty: Intermediate
---

## Statement

Count the ways to choose exactly `k` positions from `nums` so that the chosen values add up to `target`. Two choices are different if they use different positions, even when the values are equal.

Choosing zero items (`k = 0`) gives exactly one way, with sum `0`.

### Examples

**Example 1**

Input:

```python
count_subset_sums([1, 2, 3, 4], 2, 5)
```

Output:

```text
2
```

The positions with values (1, 4) and (2, 3).

**Example 2**

Input:

```python
count_subset_sums([2, 2, 2], 2, 4)
```

Output:

```text
3
```

Every pair of positions works: 3 ways.

### Constraints

- `0 <= len(nums) <= 22`
- `0 <= k <= len(nums)`
- `-100 <= nums[i] <= 100`
- `-2200 <= target <= 2200`

## Theory

When `n` is small, trying all the choices is the right answer, and the work is how you enumerate them. `itertools.combinations(items, k)` yields every way to pick `k` items without repeats, in order, without writing nested loops. There are `C(n, k)` of them: for `n = 22` and `k = 11` that is 705,432, fine for a computer, impossible by hand.

Related tools in `itertools`: `permutations` (order matters), `product` (cartesian product, with repeats), `combinations_with_replacement`. Knowing which one matches a problem saves a lot of recursion code.

## Explanation

`combinations(nums, k)` picks positions, so equal values at different positions are different choices, as the problem wants. Count those with `sum(c) == target`.

For `k = 0` it yields one empty tuple whose sum is `0`.
