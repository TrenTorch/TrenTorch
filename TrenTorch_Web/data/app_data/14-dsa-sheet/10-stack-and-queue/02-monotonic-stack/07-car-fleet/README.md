---
name: sheet-car-fleet
title: 'Car Fleet'
tags: [dsa-sheet, stack-and-queue, monotonic-stack]
difficulty: Advanced
theory: cars-that-cannot-overtake
---

## Statement

Cars drive on a one-lane road towards a `target` at mile `target`. Each car is a pair `[position, speed]`: it starts at `position` (all different, all below `target`) and drives at a constant `speed`. A car **cannot overtake**: when a faster car catches up to a slower one it slows down and drives right behind it, and they continue as a **fleet** (at the speed of the slowest). A single car is a fleet too.

Return the **number of fleets** that arrive at the target.

For `target = 12` and `cars = [[10, 2], [8, 4], [0, 1], [5, 1], [3, 3]]` the answer is `3`.

### Examples

**Example 1**

Input:

```python
car_fleet(12, [[10, 2], [8, 4], [0, 1], [5, 1], [3, 3]])
```

Output:

```text
3
```

**Example 2**

Input:

```python
car_fleet(10, [[3, 3]])
```

Output:

```text
1
```

### Constraints

- `0 <= number of cars <= 200000`
- `0 <= position < target <= 10**9`, all positions different
- `1 <= speed <= 10**6`

## Explanation

After sorting from the car nearest the target, `slow_num / slow_den` is the arrival time of the fleet ahead. A car needing more time than that starts a new fleet. Exact fractions are compared by cross-multiplying.

### Complexity

- Time: O(n log n). Sorting the cars by position dominates; the scan is one pass.
- Space: O(n). The sorted list.
