---
name: sheet-next-greater-circular
title: 'Next Greater Element in a Circle'
tags: [dsa-sheet, stack-and-queue, monotonic-stack]
difficulty: Intermediate
---

## Statement

The list is **circular**: after the last element comes the first one again. For each value, find the **next strictly greater value**, looking to the right and wrapping around the end if needed; return `-1` if there is none.

For `[1, 2, 1]` the answer is `[2, -1, 2]`.

### Examples

**Example 1**

Input:

```python
next_greater_circular([1, 2, 1])
```

Output:

```text
[2, -1, 2]
```

**Explanation:** For 1 at index 0 the next greater to the right is 2 at index 1; for 2 at index 1 there is no greater element in the circle; for 1 at index 2 wrapping around gives 2 at index 1.

**Example 2**

Input:

```python
next_greater_circular([1, 2, 3, 4, 3])
```

Output:

```text
[2, 3, 4, -1, 4]
```

**Explanation:** For 1 the next greater is 2; for 2 the next greater is 3; for 3 at index 2 the next greater is 4; for 4 there is no greater; for the last 3 wrapping gives 4.

### Constraints

- `0 <= len(nums) <= 200000`
- `-10**9 <= nums[i] <= 10**9`

## Theory

A **stack** is last in, first out: you only add (`push`) and remove (`pop`) at the top. In Python a list does this with `append()` and `pop()`, both `O(1)`.

A circle can be handled by **walking the list twice**. Run the usual monotonic stack over indices `0 .. 2n - 1`, using `nums[i % n]` as the value. Only push an index in the first lap (`i < n`): the second lap is only there to answer the indices still waiting.

Everything else is the same as in the plain next greater element question. `O(n)`.

## Explanation

In the second lap values only answer waiting indices; they are not pushed again, so every index is answered at most once.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line          | Variables                                     |
| ------------------------ | --------------------------------------------- |
| `n = len(nums)`          | `n = 3`                                       |
| `for i in range(2 * n):` | `out = [-1, -1, -1], stack = [], i = 0`       |
| `stack.append(i)`        | `stack = [0], x = 1`                          |
| `out[stack.pop()] = x`   | `out = [2, -1, -1], stack = [], i = 1, x = 2` |
| `x = nums[i % n]`        | `stack = [1], i = 2, x = 1`                   |
| `for i in range(2 * n):` | `stack = [1, 2], i = 4`                       |
| `out[stack.pop()] = x`   | `out = [2, -1, 2], stack = [1], x = 2`        |
| `return`                 | `returned = [2, -1, 2]`                       |

### Complexity

- Time: O(n) where n is the length of nums.
- Extra space: O(n) for the output and stack.
- The brute force takes O(n^2) where n is the length of nums.
