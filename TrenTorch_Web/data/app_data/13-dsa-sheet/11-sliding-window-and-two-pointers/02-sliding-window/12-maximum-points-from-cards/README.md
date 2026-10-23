---
name: sheet-maximum-points-from-cards
title: 'Maximum Points From Cards'
tags: [dsa-sheet, sliding-window, sliding-window]
difficulty: Intermediate
---

## Statement

Cards lie in a row, and `points[i]` is the value of card `i`. In each of `k` steps you take **one card from either the left end or the right end**. Return the **maximum total** you can reach.

For `points = [1, 2, 3, 4, 5, 6, 1]` and `k = 3` the answer is `12` (the cards `1`, `6`, `5`).

### Examples

**Example 1**

Input:

```python
max_points([1, 2, 3, 4, 5, 6, 1], 3)
```

Output:

```text
12
```

**Example 2**

Input:

```python
max_points([2, 2, 2], 2)
```

Output:

```text
4
```

### Constraints

- `1 <= k <= len(points) <= 200000`
- `-10**4 <= points[i] <= 10**4`

## Theory

A **sliding window** is a range `[left, right]` of the data that grows on the right and shrinks on the left. Because each end only moves forward, the whole pass is `O(n)`, while the window always describes one candidate subarray or substring.

Whatever you do, the `k` cards you take are always some number `i` from the **left** end and `k - i` from the **right** end. The cards you do **not** take form one contiguous block in the middle of length `n - k`.

So the problem is the same as finding the **minimum-sum window of size `n - k`** and subtracting it from the total. Slide a fixed window of size `n - k` and keep the smallest window sum. `O(n)`.

Looking at the complement (what you leave) is the key that turns "two ends" into one window.

## Explanation

`total - min_window` is the best sum of the cards taken from the ends. When `k == n` the window is empty and everything is taken.
