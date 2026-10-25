---
name: sheet-kth-largest-in-a-stream
title: 'Kth Largest in a Stream'
tags: [dsa-sheet, heaps, heap-basics]
difficulty: Intermediate
---

## Statement

Start with the values `nums`. Then add the values of `adds` **one at a time**. After each addition, report the **`k`-th largest value** among everything seen so far (counting repeated values separately). Return the list of these answers, one per addition.

For `k = 3`, `nums = [4, 5, 8, 2]` and `adds = [3, 5, 10, 9, 4]` the answer is `[4, 5, 5, 8, 8]`.

### Examples

**Example 1**

Input:

```python
kth_largest_stream(3, [4, 5, 8, 2], [3, 5, 10, 9, 4])
```

Output:

```text
[4, 5, 5, 8, 8]
```

**Explanation:** After initializing with the three largest of [4,5,8,2] (8,5,4), each added number updates the min-heap of size 3, so the heap root yields 4,5,5,8,8 respectively.

**Example 2**

Input:

```python
kth_largest_stream(1, [], [-3, -2, -4, 0, 4])
```

Output:

```text
[-3, -2, -2, 0, 4]
```

**Explanation:** With k = 1 the heap always keeps the single largest value seen, so after each addition the output becomes -3, -2, -2, 0, 4.

### Constraints

- `1 <= k <= 10000`
- `k - 1 <= len(nums) <= 100000`, so there are at least `k` values after the first addition
- `0 <= len(adds) <= 100000`
- `-10**9 <= value <= 10**9`

## Theory

A **heap** (priority queue) always gives you the **smallest** item in `O(log n)`, while letting you add items in `O(log n)`. Python's `heapq` module implements a **min-heap** on a plain list: `heappush(h, x)`, `heappop(h)` (the smallest), `h[0]` (peek) and `heapify(h)` (turn a list into a heap in `O(n)`). For a **max-heap** push the negated values.

To answer "what is the `k`-th largest", you only need to remember the **`k` largest values**, and the smallest of those is the answer. A **min-heap of size `k`** holds them with the answer on top. For a new value: if the heap has fewer than `k` items, push it; otherwise if the value is bigger than the top, replace the top (`heappushpop` or `heapreplace`). The top is the `k`-th largest.

Each addition costs `O(log k)`, while sorting every time costs `O(n log n)`. This pattern, "top `k` with a min-heap of size `k`", appears again and again.

## Explanation

The heap is built from the starting values by keeping only the `k` largest. After that `heappushpop` adds the new value and removes the smallest of the `k + 1`, leaving the `k` largest.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line              | Variables                                      |
| ---------------------------- | ---------------------------------------------- |
| `heap = []`                  | `heap = []`                                    |
| `for x in nums:`             | `heap = [4], x = 5`                            |
| `for x in nums:`             | `heap = [4, 5, 8], x = 2`                      |
| `out = []`                   | `out = []`                                     |
| `heapq.heappushpop(heap, x)` | `heap = [5, 5, 8], x = 5, out = [4]`           |
| `heapq.heappushpop(heap, x)` | `heap = [5, 10, 8], x = 10, out = [4, 5]`      |
| `out.append(heap[0])`        | `heap = [8, 10, 9], x = 9, out = [4, 5, 5, 8]` |
| `return`                     | `returned = [4, 5, 5, 8, 8]`                   |

### Complexity

- Time: O((n+q) log k), n is initial count, q is adds.
- Extra space: O(k), extra heap size.
- The brute force takes O(q * (n+q) log (n+q)), q adds.
