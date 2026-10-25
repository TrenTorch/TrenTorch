---
name: sheet-three-sum-smaller
title: 'Count Triplets With a Smaller Sum'
tags: [dsa-sheet, two-pointers, two-pointers]
difficulty: Intermediate
---

## Statement

Return the number of **triples of positions** `i < j < k` with `nums[i] + nums[j] + nums[k] < target`.

For `nums = [-2, 0, 1, 3]` and `target = 2` the answer is `2` (`-2 + 0 + 1` and `-2 + 0 + 3`).

The starter code tries every triple. It is correct but too slow for long lists.

### Examples

**Example 1**

Input:

```python
count_triplets_smaller([-2, 0, 1, 3], 2)
```

Output:

```text
2
```

**Explanation:** The two triplets with sum less than 2 are (-2,0,1) and (-2,0,3).

**Example 2**

Input:

```python
count_triplets_smaller([], 0)
```

Output:

```text
0
```

**Explanation:** No triplets exist because the list is empty.

### Constraints

- `0 <= len(nums) <= 1000`
- `-1000 <= nums[i] <= 1000`
- `-3000 <= target <= 3000`

## Theory

The order of positions does not change the sum, so sort the list: counting triples of **values** (as sets of three positions) is the same. Fix `i`, then use two pointers `lo = i + 1` and `hi = n - 1`.

If `a[i] + a[lo] + a[hi] < target`, then **every** `k` between `lo + 1` and `hi` also works with `lo` (they are smaller than `a[hi]`): add `hi - lo` triples at once, and move `lo` forward. Otherwise the sum is too big: move `hi` back.

Counting many answers in one step ("everything between the pointers also works") is the common trick in two-pointer counting questions. `O(n²)`.

## Explanation

After sorting, a successful pair `(lo, hi)` means all positions `lo+1..hi` can play the third role together with `lo`; that is `hi - lo` triples.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line               | Variables               |
| ----------------------------- | ----------------------- |
| `a = sorted(nums)`            | `a = [-2, 0, 1, 3]`     |
| `count = 0`                   | `count = 0`             |
| `lo, hi = i + 1, len(a) - 1`  | `i = 0, lo = 1, hi = 3` |
| `count += hi - lo`            | `count = 2`             |
| `hi -= 1`                     | `lo = 2, hi = 2`        |
| `for i in range(len(a) - 2):` | `i = 1`                 |
| `hi -= 1`                     | `(no change)`           |
| `return`                      | `returned = 2`          |

### Complexity

- Time: O(n^2) n is the length of nums.
- Extra space: O(n) for the sorted copy.
- The brute force takes O(n^3) n is the length of nums.
