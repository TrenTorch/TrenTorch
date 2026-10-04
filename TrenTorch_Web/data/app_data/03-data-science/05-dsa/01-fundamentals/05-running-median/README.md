---
name: dsa-running-median
title: 'Find Running Median'
tags: [dsa]
difficulty: Intermediate
---

## Statement

Compute the median after each addition: [1]→median 1, [1,2]→median 1.5, [1,2,3]→median 2. Use two heaps (max-heap for smaller half, min-heap for larger half) for O(log n) addition and O(1) median.

## Theory

### Heaps enable efficient median tracking

A naive approach (sort after each insert) is O(n log n). Heaps provide O(log n):

- Max-heap: tracks the smaller half of numbers
- Min-heap: tracks the larger half

`Example with [1, 2, 3, 4, 5]:
Smaller half (max-heap): [3, 2, 1]
Larger half (min-heap): [4, 5]
Median = (3 + 4) / 2 = 3.5`

### Invariants

- Size difference: |size(max_heap) - size(min_heap)| ≤ 1
- All elements in max-heap ≤ all elements in min-heap

### Operations

- addNum(num): insert into appropriate heap, rebalance
- findMedian(): if sizes equal, average tops; else return larger heap's top

Time: O(log n) per addition, O(1) median.

### Why this matters

- Streaming data: compute median without sorting
- Outlier detection: compare values to running median
- Time-series analysis: smoothing and trend detection

## Explanation

The solution maintains two heaps: a max-heap for the smaller half (accessible via negate in languages without max-heaps) and a min-heap for the larger half. addNum() inserts into appropriate heap and rebalances. findMedian() returns the root of the larger heap or their average.
