---
name: sheet-three-sum-closest
title: 'Three Sum Closest'
tags: [dsa-sheet, two-pointers, two-pointers]
difficulty: Intermediate
---

## Statement

Choose **three different positions** of `nums` and return the **sum that is closest to `target`**. If two sums are equally close, return the **smaller** one.

For `nums = [-1, 2, 1, -4]` and `target = 1` the answer is `2` (`-1 + 2 + 1`).

The starter code tries every triple. It is correct but too slow for long lists.

### Examples

**Example 1**

Input:

```python
three_sum_closest([-1, 2, 1, -4], 1)
```

Output:

```text
2
```

**Explanation:** The triple -1, 1, 2 sums to 2, distance 1 from target; all other triples have distance greater than 1 or equal distance but larger sum.

**Example 2**

Input:

```python
three_sum_closest([0, 0, 0], 1)
```

Output:

```text
0
```

**Explanation:** Only triple is three zeros summing to 0, distance 1 from target, so 0 is returned.

### Constraints

- `3 <= len(nums) <= 1000`
- `-1000 <= nums[i] <= 1000`
- `-3000 <= target <= 3000`

## Theory

**Two pointers** means keeping two positions in the data (often one at each end, or one behind the other) and moving them according to a rule, so that each position moves at most `n` times in total. That turns a double loop (`O(n²)`) into a single pass (`O(n)`).

Sort `nums`. Fix the first number `nums[i]`; the other two come from the rest, which is sorted, so use **two pointers** `lo` (just after `i`) and `hi` (the end). The sum `s = nums[i] + nums[lo] + nums[hi]` tells which pointer to move: if `s < target` a bigger sum is needed, so `lo += 1`; if `s > target`, `hi -= 1`; if `s == target`, you cannot do better. Keep the best sum seen.

The loop over `i` is `O(n)` and each pointer pass is `O(n)`: `O(n²)` overall, instead of `O(n³)` for all triples.

## Explanation

Ties go to the smaller sum with the key `(abs(s - target), s)`. Each pointer pass moves `lo` or `hi` until they meet.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                  | Variables                            |
| -------------------------------- | ------------------------------------ |
| `a = sorted(nums)`               | `a = [-4, -1, 1, 2]`                 |
| `lo, hi = i + 1, len(a) - 1`     | `best = -4, i = 0, lo = 1, hi = 3`   |
| `best_diff = abs(best - target)` | `s = -3, diff = 4, best_diff = 5`    |
| `s = a[i] + a[lo] + a[hi]`       | `best = -3, lo = 2, s = -1`          |
| `best = s`                       | `best = -1, diff = 2, best_diff = 4` |
| `lo, hi = i + 1, len(a) - 1`     | `i = 1`                              |
| `best_diff = abs(best - target)` | `s = 2, diff = 1, best_diff = 2`     |
| `return`                         | `returned = 2`                       |

### Complexity

- Time: O(n^2) where n is the length of nums.
- Extra space: O(n) extra for the sorted copy of nums.
- The brute force takes O(n^3) where n is the length of nums.
