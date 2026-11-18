---
name: sheet-count-subset-sums
title: 'Count Subsets With Sum'
tags: [dsa-sheet, basics, python-toolbox]
difficulty: Intermediate
theory: combinations-permutations-and-meeting-in-the-middle
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

## Explanation

Meet in the middle. Split `nums` into two halves. For each half, count how many of its subsets have each pair `(size, sum)`; one half has at most `2^(n/2)` subsets. A chosen subset of the whole list is one subset from each half, so for every `(size, sum)` of the right half you look up how many left subsets have `(k - size, target - sum)` and multiply the two counts.

Equal values at different positions stay different choices because subsets are built from positions. With `k = 0` the empty subset has sum `0`.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                                           | Variables                                                                  |
| --------------------------------------------------------- | -------------------------------------------------------------------------- |
| `half = len(nums) // 2`                                   | `half = 2`                                                                 |
| `left = _sums_by_size(nums[:half])`                       | `left = Counter({(0, 0): 1, (1, 1): 1, (1, 2): 1, (2, 3): 1})`             |
| `count = 0`                                               | `right = Counter({(0, 0): 1, (1, 3): 1, (1, 4): 1, (2, 7): 1}), count = 0` |
| `for (size, total), ways in right.items():`               | `size = 0, total = 0, ways = 1`                                            |
| `count += ways * left.get((k - size, target - total), 0)` | `count = 1, size = 1, total = 3`                                           |
| `for (size, total), ways in right.items():`               | `total = 4`                                                                |
| `for (size, total), ways in right.items():`               | `count = 2, size = 2, total = 7`                                           |
| `return`                                                  | `returned = 2`                                                             |

### Complexity

- Time: O(2^(n/2)). Meet in the middle: each half has at most `2^(n/2)` subsets and every right-half subset needs one dictionary lookup.
- Space: O(2^(n/2)). The dictionary of `(size, sum)` counts for the left half.
