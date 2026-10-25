---
name: sheet-two-sum-first-pair
title: 'Two Sum: First Pair'
tags: [dsa-sheet, arrays, array-patterns]
difficulty: Beginner
---

## Statement

Find two **different positions** `i < j` with `nums[i] + nums[j] == target` and return `[i, j]`.

If several pairs work, return the one with the **smallest `i`**, and among those the smallest `j`. If no pair works, return `[-1, -1]`.

The starter code checks every pair. It is correct but too slow for long lists. Make it fast.

### Examples

**Example 1**

Input:

```python
two_sum_first_pair([1, 6, 5, 3, 8], 9)
```

Output:

```text
[0, 4]
```

`1 + 8` (positions 0 and 4) and `6 + 3` (positions 1 and 3) both work. The first has the smaller `i`.

**Example 2**

Input:

```python
two_sum_first_pair([2, 4], 7)
```

Output:

```text
[-1, -1]
```

No pair adds to 7.

### Constraints

- `0 <= len(nums) <= 2 * 10**5`
- `0 <= nums[i] <= 10**9`
- `-1 <= target <= 2 * 10**9`

## Theory

Checking every pair is `O(n²)`. For each value `x` the partner you need is `target - x`, and a **dictionary** answers "is that value somewhere earlier, and where?" in `O(1)` on average.

Scan left to right. For the value at position `j`, look up `target - nums[j]` among the values seen before. Store only the **first** index of each value, because you want the smallest `i`. Every matching pair `(i, j)` is found when its `j` is reached, so keep the best pair seen using the order "smaller `i` first, then smaller `j`". Stopping at the first match found would be wrong: a later `j` can pair with an earlier `i`.

This "remember what you have seen in a dictionary" pattern is the foundation of most hashing problems.

## Explanation

`first[v]` is the first index of value `v`. For each `j`, if `target - nums[j]` has a first index `i < j`, then `(i, j)` is a candidate. The best candidate is the smallest tuple. The scan covers every `j`, so it cannot miss a pair with a smaller `i` found later.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                | Variables                                         |
| ------------------------------ | ------------------------------------------------- |
| `first = {}`                   | `first = {}`                                      |
| `for j, x in enumerate(nums):` | `best = None, j = 0, x = 1`                       |
| `for j, x in enumerate(nums):` | `first = {1: 0}, j = 1, x = 6, i = None`          |
| `for j, x in enumerate(nums):` | `first = {1: 0, 6: 1}, j = 2, x = 5`              |
| `i = first.get(target - x)`    | `first = {1: 0, 6: 1, 5: 2}, j = 3, x = 3, i = 1` |
| `first[x] = j`                 | `first = {1: 0, 6: 1, 5: 2, 3: 3}, best = (1, 3)` |
| `best = (i, j)`                | `best = (0, 4), j = 4, x = 8, i = 0`              |
| `return`                       | `returned = [0, 4]`                               |

### Complexity

- Time: O(n) where n is the length of nums.
- Extra space: O(n) for the dictionary storing first occurrences.
- The brute force takes O(n^2) where n is the length of nums.
