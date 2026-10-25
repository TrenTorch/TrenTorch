---
name: sheet-last-stone-weight
title: 'Last Stone Weight'
tags: [dsa-sheet, heaps, heap-basics]
difficulty: Beginner
---

## Statement

`stones[i]` is the weight of stone `i`. Each turn take the **two heaviest** stones and smash them together. If their weights are equal both are destroyed; otherwise the lighter one is destroyed and the heavier one keeps the **difference** of the weights. Return the weight of the **last remaining stone**, or `0` if none is left.

For `[2, 7, 4, 1, 8, 1]` the answer is `1`.

The starter code sorts all stones after every smash. It is correct but too slow for many stones.

### Examples

**Example 1**

Input:

```python
last_stone_weight([2, 7, 4, 1, 8, 1])
```

Output:

```text
1
```

**Explanation:** The two heaviest stones 8 and 7 are smashed, leaving a stone of weight 1, which continues to be smashed with other stones until only a stone of weight 1 remains.

**Example 2**

Input:

```python
last_stone_weight([1])
```

Output:

```text
1
```

**Explanation:** Only one stone remains, so no smashing occurs and the weight stays 1.

### Constraints

- `0 <= len(stones) <= 100000`
- `1 <= stones[i] <= 10**9`

## Theory

A **heap** (priority queue) always gives you the **smallest** item in `O(log n)`, while letting you add items in `O(log n)`. Python's `heapq` module implements a **min-heap** on a plain list: `heappush(h, x)`, `heappop(h)` (the smallest), `h[0]` (peek) and `heapify(h)` (turn a list into a heap in `O(n)`). For a **max-heap** push the negated values.

Each turn needs the two **largest** stones and then a new stone is added back: exactly what a max-heap is for. Put the negated weights in a heap. Pop two (the two heaviest), and if they differ, push the difference.

Sorting after every turn costs `O(n log n)` per turn, `O(n² log n)` overall; the heap makes every turn `O(log n)`, so `O(n log n)` in total.

## Explanation

`heap` holds negative weights, so `heappop` returns the heaviest stone. The loop runs until at most one stone remains.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                  | Variables                            |
| -------------------------------- | ------------------------------------ |
| `heap = [-s for s in stones]`    | `heap = [-2, -7, -4, -1, -8, -1]`    |
| `a = -heapq.heappop(heap)`       | `heap = [-7, -2, -4, -1, -1], a = 8` |
| `heapq.heappush(heap, -(a - b))` | `heap = [-4, -2, -1, -1, -1], b = 7` |
| `b = -heapq.heappop(heap)`       | `heap = [-1, -1, -1], a = 4, b = 2`  |
| `heapq.heappush(heap, -(a - b))` | `heap = [-2, -1, -1, -1]`            |
| `b = -heapq.heappop(heap)`       | `heap = [-1, -1], a = 2, b = 1`      |
| `a = -heapq.heappop(heap)`       | `a = 1`                              |
| `return`                         | `returned = 1`                       |

### Complexity

- Time: O(n log n) n is number of stones.
- Extra space: O(n) extra memory for heap of size n.
- The brute force takes O(n^2 log n) n is number of stones.
