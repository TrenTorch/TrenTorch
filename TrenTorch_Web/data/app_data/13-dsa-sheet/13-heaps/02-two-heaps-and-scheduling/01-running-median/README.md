---
name: sheet-running-median
title: 'Median After Each Number'
tags: [dsa-sheet, heaps, two-heaps-and-scheduling]
difficulty: Advanced
---

## Statement

Numbers arrive one at a time. After each number, report the **median** of all numbers so far: the middle one for an odd count, or the average of the two middle ones for an even count. Return the list of medians (as decimals such as `2.0` and `2.5`).

For `[5, 15, 1, 3]` the answer is `[5.0, 10.0, 5.0, 4.0]`.

### Examples

**Example 1**

Input:

```python
running_median([5, 15, 1, 3])
```

Output:

```text
[5.0, 10.0, 5.0, 4.0]
```

**Example 2**

Input:

```python
running_median([2])
```

Output:

```text
[2.0]
```

### Constraints

- `0 <= len(nums) <= 100000`
- `-10**9 <= nums[i] <= 10**9`

## Theory

A **heap** (priority queue) always gives you the **smallest** item in `O(log n)`, while letting you add items in `O(log n)`. Python's `heapq` module implements a **min-heap** on a plain list: `heappush(h, x)`, `heappop(h)` (the smallest), `h[0]` (peek) and `heapify(h)` (turn a list into a heap in `O(n)`). For a **max-heap** push the negated values.

The median splits the numbers into a **lower half** and an **upper half**. You only need the **largest of the lower half** and the **smallest of the upper half**. That calls for **two heaps**: a max-heap `low` (store negated values) for the lower half and a min-heap `high` for the upper half.

Keep them balanced: `low` has the same size as `high`, or one more. For a new number `x`: push it into `low`, then move the largest of `low` to `high` (so every value of `low` stays `<=` every value of `high`), and if `high` became bigger than `low`, move its smallest back. Then the median is the top of `low` (odd count) or the average of both tops (even count).

Each number costs `O(log n)`. Inserting into a sorted list works but costs `O(n)` per number.

## Explanation

`low` is a max-heap through negation. The two-step push keeps the order between the halves; the size check keeps them balanced so the tops are the middle values.
