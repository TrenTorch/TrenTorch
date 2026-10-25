---
name: sheet-max-consecutive-ones-iii
title: 'Longest Run of Ones After K Flips'
tags: [dsa-sheet, sliding-window, sliding-window]
difficulty: Intermediate
---

## Statement

`nums` contains only `0`s and `1`s. You may flip **at most `k` zeros** to ones. Return the length of the **longest run of ones** you can get.

For `nums = [1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0]` and `k = 2` the answer is `6`.

### Examples

**Example 1**

Input:

```python
longest_ones([1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0], 2)
```

Output:

```text
6
```

**Explanation:** By flipping zeros at positions 3 and 4, the array contains a block of six consecutive ones from index 0 to 5.

**Example 2**

Input:

```python
longest_ones([0, 0, 1, 1, 1], 0)
```

Output:

```text
3
```

**Explanation:** With no flips, the longest run of existing ones is the block at the end, of length 3.

### Constraints

- `0 <= len(nums) <= 200000`
- `0 <= k <= len(nums)`

## Theory

A **sliding window** is a range `[left, right]` of the data that grows on the right and shrinks on the left. Because each end only moves forward, the whole pass is `O(n)`, while the window always describes one candidate subarray or substring.

Flipping at most `k` zeros means the window may contain **at most `k` zeros**. Slide the window: count the zeros inside; if the count goes above `k`, shrink from the left until it is back to `k`. The longest window seen is the answer.

This is the "longest valid window" template again with the condition `zeros <= k`. `O(n)`.

## Explanation

`zeros` is the number of zeros in the window. Moving `left` past a zero reduces it.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                      | Variables                                  |
| ------------------------------------ | ------------------------------------------ |
| `zeros = 0`                          | `zeros = 0`                                |
| `best = max(best, right - left + 1)` | `left = 0, best = 1, right = 0, x = 1`     |
| `for right, x in enumerate(nums):`   | `best = 3, right = 3, x = 0`               |
| `zeros += 1`                         | `zeros = 2, best = 4, right = 4`           |
| `left += 1`                          | `zeros = 3, left = 2, best = 5, right = 5` |
| `for right, x in enumerate(nums):`   | `zeros = 2, left = 4, right = 6, x = 1`    |
| `for right, x in enumerate(nums):`   | `best = 6, right = 10, x = 0`              |
| `return`                             | `returned = 6`                             |

### Complexity

- Time: O(n) n is length of nums.
- Extra space: O(1) constant auxiliary space.
- The brute force takes O(n^3) the number of array items.
