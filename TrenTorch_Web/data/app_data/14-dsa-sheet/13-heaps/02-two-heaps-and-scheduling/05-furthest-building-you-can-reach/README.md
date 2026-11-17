---
name: sheet-furthest-building-you-can-reach
title: 'Furthest Building You Can Reach'
tags: [dsa-sheet, heaps, two-heaps-and-scheduling]
difficulty: Advanced
theory: regret-again-ladders-for-the-biggest-climbs
---

## Statement

Buildings stand in a row with `heights[i]`. You start on building 0 and move to the next building each step. If the next building is **not higher**, you just walk. If it is higher, you must climb using **bricks** (the number of bricks equals the height difference) or **one ladder** (any height, ladders are used up). Return the **index of the furthest building** you can reach.

For `heights = [4, 2, 7, 6, 9, 14, 12]`, `bricks = 5` and `ladders = 1` the answer is `4`.

The starter code sorts all the climbs again for each building. It is correct but too slow for many buildings.

### Examples

**Example 1**

Input:

```python
furthest_building([4, 2, 7, 6, 9, 14, 12], 5, 1)
```

Output:

```text
4
```

**Example 2**

Input:

```python
furthest_building([4, 12, 2, 7, 3, 18, 20, 3, 19], 10, 2)
```

Output:

```text
7
```

### Constraints

- `1 <= len(heights) <= 100000`
- `1 <= heights[i] <= 10**6`
- `0 <= bricks <= 10**9`
- `0 <= ladders <= len(heights)`

## Explanation

`heap` holds the climbs currently covered by ladders. When it grows beyond `ladders`, the smallest is moved to bricks (`bricks -= popped`). Negative bricks means this step cannot be done.

### Complexity

- Time: O(n log L). A min-heap of the `L` biggest climbs (the ones that get ladders); each climb is pushed and popped at most once.
- Space: O(L). The heap, `L` = number of ladders.
