---
name: sheet-running-median
title: 'Median After Each Number'
tags: [dsa-sheet, heaps, two-heaps-and-scheduling]
difficulty: Advanced
theory: adding-a-number
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

## Explanation

`low` is a max-heap through negation. The two-step push keeps the order between the halves; the size check keeps them balanced so the tops are the middle values.

### Complexity

- Time: O(n log n). Two heaps keep the lower and the upper half, `O(log n)` per value.
- Space: O(n). The two heaps.
