---
name: sheet-house-robber
title: 'House Robber'
tags: [dsa-sheet, dynamic-programming, sequences-and-counting]
difficulty: Beginner
---

## Statement

`nums[i]` is the money in house `i`. You may rob any houses, but **never two neighbouring houses**. Return the **largest total** you can take.

For `[2, 7, 9, 3, 1]` the answer is `12` (rob 2, 9 and 1).

The starter code tries both choices for every house. It is correct but too slow for many houses.

### Examples

**Example 1**

Input:

```python
rob([1, 2, 3, 1])
```

Output:

```text
4
```

**Explanation:** The largest total is achieved by robbing houses 0 and 2, yielding 1+3=4

**Example 2**

Input:

```python
rob([2, 7, 9, 3, 1])
```

Output:

```text
12
```

**Explanation:** The optimum is 2+9+1=12 by selecting nonadjacent houses 0,2,4

### Constraints

- `0 <= len(nums) <= 1000000`
- `0 <= nums[i] <= 10000`

## Theory

**Dynamic programming (DP)** solves a problem by combining the answers to smaller versions of the same problem and **remembering** them, so each smaller version is solved only once. It works when the plain recursion keeps asking the same questions (**overlapping subproblems**) and the best answer is built from best answers of smaller parts (**optimal substructure**). The recipe: pick the **state** (what identifies one subproblem), write the **transition** (how a state's answer comes from smaller states), set the **base cases**, and choose the **order**: top-down recursion with a cache, or a bottom-up table. A table often needs only its last row or last few values, which saves memory.

**State:** `best(i)`, the most money from the first `i` houses. **Transition:** for house `i` you either skip it (`best(i - 1)`) or rob it, which forbids house `i - 1` (`best(i - 2) + nums[i - 1]`): `best(i) = max(best(i - 1), best(i - 2) + nums[i - 1])`. **Base cases:** `best(0) = 0`, `best(1) = nums[0]`.

The plain recursion has two branches per house, `O(2^n)` calls, although there are only `n` different states. With the table (or two variables) it is `O(n)`.

## Explanation

`skip` is `best(i - 1)` and `take` is `best(i - 2)`; each round computes the new best and shifts.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                          | Variables                   |
| ---------------------------------------- | --------------------------- |
| `skip = take = 0`                        | `skip = 0, take = 0`        |
| `for x in nums:`                         | `x = 1`                     |
| `for x in nums:`                         | `take = 1, x = 2`           |
| `skip, take = max(skip, take), skip + x` | `skip = 1, take = 2`        |
| `for x in nums:`                         | `x = 3`                     |
| `skip, take = max(skip, take), skip + x` | `skip = 2, take = 4`        |
| `skip, take = max(skip, take), skip + x` | `skip = 4, take = 3, x = 1` |
| `return`                                 | `returned = 4`              |

### Complexity

- Time: O(n).
- Extra space: O(1).
- The brute force takes O(2^n).
