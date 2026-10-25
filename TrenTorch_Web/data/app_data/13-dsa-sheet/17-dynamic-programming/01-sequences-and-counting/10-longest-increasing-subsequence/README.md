---
name: sheet-longest-increasing-subsequence
title: 'Longest Increasing Subsequence'
tags: [dsa-sheet, dynamic-programming, sequences-and-counting]
difficulty: Advanced
---

## Statement

Return the length of the **longest strictly increasing subsequence** of `nums` (a subsequence keeps the order but may skip values).

For `[10, 9, 2, 5, 3, 7, 101, 18]` the answer is `4` (`2, 3, 7, 18`).

The starter code compares every value with all earlier ones. It is correct but too slow for long lists.

### Examples

**Example 1**

Input:

```python
length_of_lis([10, 9, 2, 5, 3, 7, 101, 18])
```

Output:

```text
4
```

**Explanation:** The array contains 8 numbers, the algorithm finds an increasing subsequence of 4 elements, so length 4.

**Example 2**

Input:

```python
length_of_lis([7, 7, 7, 7])
```

Output:

```text
1
```

**Explanation:** All four numbers are equal, no increasing pair, thus LIS length 1.

### Constraints

- `0 <= len(nums) <= 200000`
- `-10**9 <= nums[i] <= 10**9`

## Theory

**Dynamic programming (DP)** solves a problem by combining the answers to smaller versions of the same problem and **remembering** them, so each smaller version is solved only once. It works when the plain recursion keeps asking the same questions (**overlapping subproblems**) and the best answer is built from best answers of smaller parts (**optimal substructure**). The recipe: pick the **state** (what identifies one subproblem), write the **transition** (how a state's answer comes from smaller states), set the **base cases**, and choose the **order**: top-down recursion with a cache, or a bottom-up table. A table often needs only its last row or last few values, which saves memory.

The standard DP: `best(i)` is the length of the longest increasing subsequence **ending at** `i`; `best(i) = 1 + max(best(j))` over `j < i` with `nums[j] < nums[i]`. That is `O(n²)`.

A cleverer method gives `O(n log n)`. Keep a list `tails` where `tails[k]` is the **smallest possible last value** of an increasing subsequence of length `k + 1`. The list stays sorted. For each new value `x`, use **binary search** to find the first entry `>= x`: replace it with `x` (a smaller ending is always better), or append `x` if all entries are smaller. The length of `tails` is the answer. (`tails` is not itself the subsequence, only its length is meaningful.)

## Explanation

`bisect_left` finds the position where `x` belongs. Using `bisect_left` (not `bisect_right`) makes equal values replace each other, which enforces strictly increasing.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line             | Variables                                |
| --------------------------- | ---------------------------------------- |
| `tails = []`                | `tails = []`                             |
| `tails.append(x)`           | `tails = [10], x = 10, i = 0`            |
| `for x in nums:`            | `tails = [9], x = 2`                     |
| `i = bisect_left(tails, x)` | `tails = [2], x = 5, i = 1`              |
| `tails[i] = x`              | `tails = [2, 3], x = 3`                  |
| `tails.append(x)`           | `tails = [2, 3, 7], x = 7, i = 2`        |
| `tails.append(x)`           | `tails = [2, 3, 7, 101], x = 101, i = 3` |
| `return`                    | `returned = 4`                           |

### Complexity

- Time: O(n log n), n is number of elements.
- Extra space: O(n), n is number of elements.
- The brute force takes O(n^2), n is number of elements.
