---
name: sheet-sum-of-subarray-minimums
title: 'Sum of Subarray Minimums'
tags: [dsa-sheet, stack-and-queue, monotonic-stack]
difficulty: Advanced
---

## Statement

Return the **sum of `min(subarray)` over every contiguous subarray** of `arr`, modulo `10**9 + 7`.

For `[3, 1, 2, 4]` the subarray minimums are `3, 1, 2, 4, 1, 1, 2, 1, 1, 1`, whose sum is `17`.

The starter code visits every subarray. It is correct but too slow for long arrays.

### Examples

**Example 1**

Input:

```python
sum_subarray_mins([3, 1, 2, 4])
```

Output:

```text
17
```

**Explanation:** Each value is counted once for every subarray in which it is the smallest: 3 once, 1 six times, 2 twice and 4 once. That is 3 + 6 + 4 + 4 = 17.

**Example 2**

Input:

```python
sum_subarray_mins([11, 81, 94, 43, 3])
```

Output:

```text
444
```

**Explanation:** Counting each value over the subarrays where it is the smallest: 11 four times, 81 twice, 94 once, 43 three times and 3 five times (it is the last element and the smallest). That is 44 + 162 + 94 + 129 + 15 = 444.

### Constraints

- `0 <= len(arr) <= 200000`
- `1 <= arr[i] <= 30000`

## Theory

A **stack** is last in, first out: you only add (`push`) and remove (`pop`) at the top. In Python a list does this with `append()` and `pop()`, both `O(1)`.

Flip the question: instead of finding the minimum of each subarray, ask **for how many subarrays is `arr[i]` the minimum?** The contribution of `arr[i]` is `arr[i] * (number of such subarrays)`.

`arr[i]` is the minimum of a subarray that starts after the previous smaller element (index `left`) and ends before the next smaller-or-equal element (index `right`). There are `i - left` choices for the start and `right - i` choices for the end, so `(i - left) * (right - i)` subarrays. (Use "strictly smaller" on one side and "smaller or equal" on the other so that equal values do not count a subarray twice.)

Both borders come from a monotonic stack: `left` is the previous strictly smaller element and `right` the next smaller-or-equal. `O(n)`.

## Explanation

One stack pass computes `left` while scanning and `right` when elements are popped; here both are computed with two passes for clarity.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                        | Variables                                                        |
| -------------------------------------- | ---------------------------------------------------------------- |
| `n = len(arr)`                         | `n = 4`                                                          |
| `for i in range(n):`                   | `left = [0, 0, 0, 0], right = [0, 0, 0, 0], stack = [], i = 0`   |
| `left[i] = stack[-1] if stack else -1` | `left = [-1, -1, 0, 0], i = 1`                                   |
| `stack.append(i)`                      | `left = [-1, -1, 1, 0], stack = [1, 2], i = 2`                   |
| `right[i] = stack[-1] if stack else n` | `left = [-1, -1, 1, 2], right = [0, 0, 0, 4], stack = [], i = 3` |
| `right[i] = stack[-1] if stack else n` | `right = [0, 0, 4, 4], i = 2`                                    |
| `stack.append(i)`                      | `right = [0, 4, 4, 4], stack = [1], i = 1`                       |
| `return`                               | `returned = 17`                                                  |

### Complexity

- Time: O(n) where n is array length.
- Extra space: O(n) extra memory for two arrays.
- The brute force takes O(n^2) time, looping over all subarrays.
