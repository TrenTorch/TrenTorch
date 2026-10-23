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

**Example 2**

Input:

```python
longest_ones([0, 0, 1, 1, 1], 0)
```

Output:

```text
3
```

### Constraints

- `0 <= len(nums) <= 200000`
- `0 <= k <= len(nums)`

## Theory

A **sliding window** is a range `[left, right]` of the data that grows on the right and shrinks on the left. Because each end only moves forward, the whole pass is `O(n)`, while the window always describes one candidate subarray or substring.

Flipping at most `k` zeros means the window may contain **at most `k` zeros**. Slide the window: count the zeros inside; if the count goes above `k`, shrink from the left until it is back to `k`. The longest window seen is the answer.

This is the "longest valid window" template again with the condition `zeros <= k`. `O(n)`.

## Explanation

`zeros` is the number of zeros in the window. Moving `left` past a zero reduces it.
