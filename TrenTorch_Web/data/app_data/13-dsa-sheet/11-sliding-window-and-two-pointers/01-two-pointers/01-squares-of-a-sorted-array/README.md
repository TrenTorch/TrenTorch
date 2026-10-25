---
name: sheet-squares-of-a-sorted-array
title: 'Squares of a Sorted Array'
tags: [dsa-sheet, two-pointers, two-pointers]
difficulty: Beginner
---

## Statement

`nums` is sorted in increasing order and may contain negative numbers. Return the **square of each number**, also sorted in increasing order, in `O(n)` time (sorting the squares works but takes `O(n log n)`).

For `[-4, -1, 0, 3, 10]` the answer is `[0, 1, 9, 16, 100]`.

### Examples

**Example 1**

Input:

```python
sorted_squares([-4, -1, 0, 3, 10])
```

Output:

```text
[0, 1, 9, 16, 100]
```

**Explanation:** The largest squares are at the extremes, so the algorithm fills the output array from back to front.

**Example 2**

Input:

```python
sorted_squares([-7, -3, 2, 3, 11])
```

Output:

```text
[4, 9, 9, 49, 121]
```

**Explanation:** Comparing absolute values of -7 and 11 identifies 121 as the largest square value.

### Constraints

- `0 <= len(nums) <= 200000`
- `-10**4 <= nums[i] <= 10**4`
- `nums` is sorted in increasing order.

## Theory

**Two pointers** means keeping two positions in the data (often one at each end, or one behind the other) and moving them according to a rule, so that each position moves at most `n` times in total. That turns a double loop (`O(n²)`) into a single pass (`O(n)`).

The biggest square is at one of the two **ends** of `nums`: the most negative number or the largest positive number. So put one pointer at each end, compare `|left|` and `|right|`, and write the bigger square into the answer from the **back**, moving that pointer inwards. Repeat until the pointers cross.

Filling from the back is the trick: you always know the next largest square, so no sorting is needed.

## Explanation

`out[i]` is filled from the last index down. The pointer with the larger absolute value supplies the next square and moves inwards.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                          | Variables                                   |
| ---------------------------------------- | ------------------------------------------- |
| `out = [0] * len(nums)`                  | `out = [0, 0, 0, 0, 0]`                     |
| `for i in range(len(nums) - 1, -1, -1):` | `left = 0, right = 4, i = 4`                |
| `for i in range(len(nums) - 1, -1, -1):` | `out = [0, 0, 0, 0, 100], right = 3, i = 3` |
| `left += 1`                              | `out = [0, 0, 0, 16, 100], left = 1`        |
| `out[i] = nums[right] ** 2`              | `out = [0, 0, 9, 16, 100], i = 2`           |
| `for i in range(len(nums) - 1, -1, -1):` | `right = 2, i = 1`                          |
| `for i in range(len(nums) - 1, -1, -1):` | `out = [0, 1, 9, 16, 100], left = 2, i = 0` |
| `return`                                 | `returned = [0, 1, 9, 16, 100]`             |

### Complexity

- Time: O(n) where n is the number of elements in nums.
- Extra space: O(n) for the output array.
- The brute force takes O(n log n) due to the sorting step.
