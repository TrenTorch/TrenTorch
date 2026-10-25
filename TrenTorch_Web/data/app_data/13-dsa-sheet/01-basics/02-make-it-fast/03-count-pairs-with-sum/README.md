---
name: sheet-count-pairs-with-sum
title: 'Count Pairs With Sum'
tags: [dsa-sheet, basics, make-it-fast]
difficulty: Intermediate
---

## Statement

Given a list of integers `nums` and an integer `target`, return how many pairs of positions `i < j` have `nums[i] + nums[j] == target`.

Pairs are counted by position, so equal values at different positions count separately.

The starter code checks every pair. Make it fast.

### Examples

**Example 1**

Input:

```python
count_pairs_with_sum([1, 2, 3, 4, 3], 6)
```

Output:

```text
2
```

Positions (1, 3) give 2 + 4 and positions (2, 4) give 3 + 3.

**Example 2**

Input:

```python
count_pairs_with_sum([2, 2, 2], 4)
```

Output:

```text
3
```

All three pairs of positions sum to 4.

### Constraints

- `0 <= len(nums) <= 2 * 10**5`
- `-10**9 <= nums[i], target <= 10**9`
- The answer can exceed `10**10`.

## Theory

Checking all pairs is `O(n²)`. Instead of asking "which earlier number pairs with this one?" by scanning, ask a table.

For each number `x`, the partner it needs is `target - x`. If you keep a `Counter` (a dictionary from value to how many times it appeared so far), then the number of earlier partners is a single lookup. Add that to the answer, then record `x`. One pass: `O(n)`.

Counting before recording matters: it makes each pair counted once and stops a number from pairing with itself.

## Explanation

Go left to right. When you reach `x`, every earlier element equal to `target - x` forms a valid pair with it, and there are `seen[target - x]` of them. Add that, then do `seen[x] += 1`.

`Counter` returns `0` for missing keys, so no extra check is needed. Updating after the lookup avoids pairing an element with itself.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line             | Variables                                             |
| --------------------------- | ----------------------------------------------------- |
| `seen = Counter()`          | `seen = Counter()`                                    |
| `for x in nums:`            | `count = 0, x = 1`                                    |
| `for x in nums:`            | `seen = Counter({1: 1}), x = 2`                       |
| `for x in nums:`            | `seen = Counter({1: 1, 2: 1}), x = 3`                 |
| `for x in nums:`            | `seen = Counter({1: 1, 2: 1, 3: 1}), x = 4`           |
| `seen[x] += 1`              | `seen = Counter({1: 1, 2: 1, 3: 1, 4: 1}), count = 1` |
| `count += seen[target - x]` | `count = 2, x = 3`                                    |
| `return`                    | `returned = 2`                                        |

### Complexity

- Time: O(n) where n is the length of nums.
- Extra space: O(n) where n is the length of nums.
- The brute force takes O(n^2) where n is the length of nums.
