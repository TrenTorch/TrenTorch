---
name: sheet-furthest-building-you-can-reach
title: 'Furthest Building You Can Reach'
tags: [dsa-sheet, heaps, two-heaps-and-scheduling]
difficulty: Advanced
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

**Explanation:** In example 1, the optimal strategy is to use 1 ladder for the climb from index 2 to 3 (height 7 to 6), and 5 bricks for the climb from index 4 to 5 (height 9 to 14), stopping at the end of index 4 because there aren't enough resources to proceed.

**Example 2**

Input:

```python
furthest_building([4, 12, 2, 7, 3, 18, 20, 3, 19], 10, 2)
```

Output:

```text
7
```

**Explanation:** In example 2, the optimal strategy is to use 2 ladders for the climbs from index 1 to 2 and index 5 to 6, and the 10 bricks are sufficient for the smaller climbs, allowing the person to reach the end of index 7 before running out of resources.

### Constraints

- `1 <= len(heights) <= 100000`
- `1 <= heights[i] <= 10**6`
- `0 <= bricks <= 10**9`
- `0 <= ladders <= len(heights)`

## Theory

A **heap** (priority queue) always gives you the **smallest** item in `O(log n)`, while letting you add items in `O(log n)`. Python's `heapq` module implements a **min-heap** on a plain list: `heappush(h, x)`, `heappop(h)` (the smallest), `h[0]` (peek) and `heapify(h)` (turn a list into a heap in `O(n)`). For a **max-heap** push the negated values.

Ladders are best spent on the **biggest** climbs, since they cover any height; bricks are best on the small ones. But you only learn the climbs as you go, so decide **later**: when you meet a climb, tentatively use a ladder on it. Keep the climbs that currently have a ladder in a **min-heap**. When you have used more ladders than you own, take the **smallest** climb off its ladder and pay for it with bricks. If the bricks run out, you cannot go further: return the current index.

That keeps the `ladders` largest climbs on ladders and the rest on bricks at every moment. `O(n log L)`.

## Explanation

`heap` holds the climbs currently covered by ladders. When it grows beyond `ladders`, the smallest is moved to bricks (`bricks -= popped`). Negative bricks means this step cannot be done.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                       | Variables                         |
| ------------------------------------- | --------------------------------- |
| `heap = []`                           | `heap = []`                       |
| `climb = heights[i] - heights[i - 1]` | `i = 1, climb = -2`               |
| `heapq.heappush(heap, climb)`         | `heap = [5], i = 2, climb = 5`    |
| `climb = heights[i] - heights[i - 1]` | `i = 3, climb = -1`               |
| `climb = heights[i] - heights[i - 1]` | `i = 4, climb = 3`                |
| `bricks -= heapq.heappop(heap)`       | `bricks = 2`                      |
| `heapq.heappush(heap, climb)`         | `heap = [5, 5], i = 5, climb = 5` |
| `return`                              | `returned = 4`                    |

### Complexity

- Time: O(n log q).
- Extra space: O(q).
- The brute force takes O((n + q) log q).
